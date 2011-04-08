# a package

from trac.core import Component, implements, ExtensionPoint
from trac.admin.api import IAdminCommandProvider
from trac.ticket.model import Ticket

class NukeUserCommand(Component):

    implements(IAdminCommandProvider)

    # IAdminCommandProvider methods
    def get_admin_commands(self):
        """Return a list of available admin commands.

        The items returned by this function must be tuples of the form
        `(command, args, help, complete, execute)`, where `command` contains
        the space-separated command and sub-command names, `args` is a string
        describing the command arguments and `help` is the help text. The
        first paragraph of the help text is taken as a short help, shown in the
        list of commands.

        `complete` is called to auto-complete the command arguments, with the
        current list of arguments as its only argument. It should return a list
        of relevant values for the last argument in the list.

        `execute` is called to execute the command, with the command arguments
        passed as positional arguments.
        """
        help = """\
               Remove the specified user

               (and in future, all their tickets)
        """
        complete = self._complete_username
        yield ('nukeusers', '<userid> ...', help, complete, self.nuke_users)

    def _complete_username(self, args):
        if len(args) < 1:
            return []
        name = args[-1] + '%'
        db = self.env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute('SELECT name FROM auth_cookie WHERE name LIKE %s', (name,))
        names = [row[0] for row in cursor.fetchall()]
        return names

    def nuke_users(self, *usernames):
        for name in usernames:
            self.nuke_user(name)

    def nuke_user(self, username):
        db = self.env.get_db_cnx()
        cursor = db.cursor()
        print "Nuking %r..." % username

        cursor.execute('SELECT id FROM ticket WHERE reporter=%s', (username,))
        ticketids = [row[0] for row in cursor.fetchall()]
        if ticketids:
            print "deleting tickets %s reported by %s" % (ticketids, username)
            for id_ in ticketids:
                Ticket(self.env, id_).delete()
        else:
            print "No tickets reported by", username
        cursor.execute("SELECT ticket,time FROM ticket_change WHERE author=%s AND field = 'comment'", (username,))

        comments = cursor.fetchall()
        if comments:
            # XXX is there an API for this? can't find one.
            print "deleting comments %s by %s" % (comments, username)
            cursor.execute("DELETE FROM ticket_change WHERE author=%s AND field = 'comment'", (username,))
        else:
            print "No comments by", username

        # Hooking into TracSpamFilter here.
        # Train all entries for this user, then delete.
        try:
            import tracspamfilter
        except ImportError:
            pass
        else:
            from tracspamfilter.api import FilterSystem
            handler =  FilterSystem(self.compmgr)
            class fakerequest(object):
                # stuff needed by Request(); the filter builds a new one
                # and it assumes it was triggered by an HTTP request.
                environ = {'wsgi.url_scheme': 'http'}
            # Unfortunately, tracspamfilter.model.LogEntry.select()
            # doesn't support querying by author. Not much of an ORM, eh?
            cursor.execute("SELECT id FROM spamfilter_log WHERE author=%s",
                           (username,))
            entries = [row[0] for row in cursor.fetchall()]

            # Bug: For some reason this hangs on handler.train(),
            # likely upstream services being slow?
            print "Training and deleting %d spamfilter log entries" % len(entries)
            for entry in entries:
                print "Training %s..." % entry
                handler.train(fakerequest, entry, spam=True)
            cursor.execute("DELETE FROM spamfilter_log WHERE author=%s",
                           (username,))


        import acct_mgr.api
        account_mgr = acct_mgr.api.AccountManager(self.env)
        delete_enabled = account_mgr.supports('delete_user')
        if delete_enabled:
            account_mgr.delete_user(username)
            # XXX auth_cookie rows do not actually seem to get deleted?
            # is there an API for this?
            cursor.execute('DELETE FROM auth_cookie WHERE name=%s', (username,))
            print "Deleted %r!" % username
        else:
            print "The password store does not support deleting users."
