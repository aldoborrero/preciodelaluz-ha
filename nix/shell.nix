{
  perSystem = {
    lib,
    pkgs-unstable,
    ...
  }:
    with lib;
    with builtins; {
      devshells.default = {
        name = "preciodelaluz-ha";
        packages = with pkgs-unstable; [
          httpie
          mitmproxy
          mitmproxy2swagger
          poetry
          python311
          stdenv
        ];
        commands = let
          poetryCommand = {
            bin,
            args ? ["$@"],
          }: {
            category = "python";
            name = "${bin}";
            help = "Run ${bin}";
            command = "poetry run ${bin} ${concatStringsSep " " args}";
          };
          commandList = [
            {bin = "pytest";}
          ];
        in
          map poetryCommand commandList;
        env = [
          {
            name = "LD_LIBRARY_PATH";
            value = "${makeLibraryPath (with pkgs-unstable; [
              stdenv.cc.cc.lib
            ])}";
          }
        ];
      };
    };
}
