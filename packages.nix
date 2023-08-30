{
  perSystem = {
    pkgs,
    lib,
    ...
  }: {
    packages = {
      preciodelaluz-ha = pkgs.stdenv.mkDerivation {
        pname = "preciodelaluz-ha";
        version = "0.1.0";

        src = pkgs.nix-gitignore.gitignoreSourcePure [./.gitignore] ./.;

        dontBuild = true;
        dontConfigure = true;

        installPhase = ''
          mkdir -p "$out/"
          cp -R ./custom_components/preciodelaluz/* "$out/"
        '';

        meta = with pkgs.lib; {
          homepage = "https://github.com/aldoborrero/preciodelaluz-ha";
          description = "Access PrecioDeLaLuz API within Home-Assistant";
          license = licenses.mit;
          maintainers = with maintainers; [aldoborrero];
        };
      };

      preciodelaluz-cli = pkgs.python311Packages.buildPythonPackage {
        pname = "preciodelaluz-cli";
        version = "0.1.0";

        format = "pyproject";

        src = pkgs.nix-gitignore.gitignoreSourcePure [./.gitignore] ./.;

        nativeBuildInputs = with pkgs.python311Packages; [
          poetry-core
        ];

        meta = with pkgs.lib; {
          homepage = "https://github.com/aldoborrero/preciodelaluz-ha";
          description = "Access PrecioDeLaLuz API within Home-Assistant";
          license = licenses.mit;
          maintainers = with maintainers; [aldoborrero];
        };
      };
    };
  };
}
