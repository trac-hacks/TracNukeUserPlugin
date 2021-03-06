TracNukeUserPlugin
==================

Status
--------

I (slinkp) am currently (Sept 2012) not using Trac at all, so I'm very unlikely
to do any more work on this, or respond to issue reports, etc.

Feel free to fork this code or do anything you like with it,
subject to the terms of the BSD license (see LICENSE.txt)

About
-------

This Trac plugin adds a single trac-admin command.  You use it like:

``trac-admin /path/to/trac/environment/  nukeusers <username> <username...>``

(If you use it interactively, it does tab-completion of usernames from
the auth cookie table in the database.)

This will do all of the following for each username:

 * Remove the user account.
 * Delete all tickets and comments created by that user.
 * Train and delete SpamFilterPlugin entries by that user.

Motivation: I've been getting some (authenticated) Trac spam lately,
some of it getting past SpamFilterPlugin's filters (I'm using all of
Akismet, BlogSpam, and reCaptcha, and they still got through).  I was
getting tired of doing cleanup manually.

It does not do anything about wiki content or attachments.  Forks are
welcome.

It does not provide a web UI. Forks welcome :)

