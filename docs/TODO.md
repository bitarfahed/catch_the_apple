# TODO

## Release Hygiene

- Add continuous integration for tests and Ruff.
- Add screenshots or short gameplay capture for the README.
- Consider executable packaging after gameplay and visuals stabilize further.

## Testing

- Add state-flow tests for menu, pause, and game-over transitions.
- Add renderer smoke tests for the full `Renderer` object.
- Add persistence migration tests if the save format changes.

## Documentation

- Keep PRDs synchronized when major mechanisms change.
- Add a troubleshooting section if platform-specific Pygame issues appear.

## Deferred Scope

- Enable additional object types only in a gameplay-focused prompt.
- Add audio assets only when licensing and file organization are addressed.
- Keep networking, database storage, and service APIs out of scope.
