Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.8.4 (2024-07-04)
------------------

Bug fixes:


- Fix duplicate serializer
  [jchandelle] (URB-3005)


1.8.3 (2024-06-27)
------------------

New features:


- Add deserializer for condition objects
  [jchandelle] (URB-3005)


1.8.2 (2024-04-22)
------------------

New features:


- Allow additional delay to be a TAL expression
  [mpeeters] (URB-3005)


Internal:


- Black
  [mpeeters] (SUP-27104)
- Fix tests
  [mpeeters] (URB-3005)


1.8.1 (2024-04-01)
------------------

- URB-3005: Add a deserializer for objects that also handle vocabulary specificities
  [mpeeters]

- URB-3005: Add converters for schedule objects
  [mpeeters]


1.8 (2023-04-06)
----------------

- Allow multiple interfaces to be registered on schedule config.
  [sdelcourt]
- Get tasks and subtasks attribute exploration rather than catalog.
  [sdelcourt]
- Add method 'get_closed_tasks' on TaskConfig.
  [sdelcourt]
- Add util method 'end_all_open_tasks' of a container.
  [sdelcourt]


1.6 (2018-08-30)
----------------

- Only display active tasks in the collection widget.
  [sdelcourt]


1.5 (2017-06-20)
----------------

- Bugfix for dashboard collection creation.
  [sdelcourt]


1.4 (2017-06-20)
----------------

- Register title colums for default dashboard collection of schedule config.
  [sdelcourt]


1.3 (2017-06-20)
----------------

- Recreate dashboard collection 'all' if its missing.
  [sdelcourt]


1.2 (2017-06-16)
----------------

- Implement an adapter for extra holidays
  [mpeeters]


1.1 (2017-04-28)
----------------

- Release on internal egge server.

- Update the compute_due_date method to handle working days
  [mpeeters]

- Add a class to manage working days for date calculation
  [mpeeters]

- Handle working days for additional delay
  [mpeeters]


1.0 (2017-04-28)
----------------

- Initial release.
  [sdelcourt]
