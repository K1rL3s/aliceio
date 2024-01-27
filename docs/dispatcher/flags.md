::: aliceio.dispatcher.flags.Flag
    handler: python
    options:
      merge_init_into_class: true
      members: true

::: aliceio.dispatcher.flags.FlagDecorator
    handler: python
    options:
      merge_init_into_class: true
      members:
        - __call__

::: aliceio.dispatcher.flags.FlagGenerator
    handler: python
    options:
      merge_init_into_class: true
      members:
        - __getattr__

::: aliceio.dispatcher.flags.extract_flags_from_object
    handler: python
    options:
      members: true

::: aliceio.dispatcher.flags.extract_flags
    handler: python
    options:
      members: true

::: aliceio.dispatcher.flags.get_flag
    handler: python
    options:
      members: true

::: aliceio.dispatcher.flags.check_flags
    handler: python
    options:
      members: true
