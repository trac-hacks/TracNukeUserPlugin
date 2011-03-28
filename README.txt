This Trac plugin adds a single trac-admin command.  You use it like:

``trac-admin /path/to/trac/environment/  nukeuser <username>``

(If you use it interactively, it does tab-completion of usernames from
the auth cookie table in the database.)

This will do all of the following:

 * Remove the user account.
 * Delete all tickets and comments created by that user.
 * Train and delete SpamFilterPlugin entries by that user.

Motivation: I've been getting some (authenticated) Trac spam lately,
some of it getting past SpamFilterPlugin's filters (I'm using all of
Akismet, BlogSpam, and reCaptcha, and they still got through).  I was
getting tired of doing cleanup manually.

It does not do anything about wiki content or attachments.  Forks and
patches welcome.

It does not provide a web UI. Forks and patches welcome :)

