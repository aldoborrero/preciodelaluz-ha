{inputs, ...}: {
  imports = [
    # flake.parts modules
    inputs.flake-root.flakeModule
    inputs.devshell.flakeModule

    # Local modules
    ./checks.nix
    ./formatter.nix
    ./shell.nix
  ];
}
