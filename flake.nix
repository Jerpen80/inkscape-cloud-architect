{
  description = "Inkscape Cloud Architect";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    cloudia-reader-aws.url = "github:wearetechnative/cloudia-reader-aws";
  };

  outputs = { self, nixpkgs, cloudia-reader-aws }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgsFor = system: import nixpkgs {
        inherit system;
      };
    in
      {
      packages = forAllSystems (system:
        let
          pkgs = pkgsFor system;
          py = pkgs.python3;
          # Symbol build toolchain + templates shipped with the package so
          # `ica setup` can build symbols on the user's machine. NOTE: built
          # AWS symbols are NOT shipped — the user supplies the AWS icon ZIP.
          symbolBuildDir = ./symbols/aws-inkscape-symbols;
          templatesDir = ./templates;
          ica = py.pkgs.buildPythonApplication {
            pname = "ica";
            version = "0.1.0";
            src = ./extensions/aws-auto-diagram;
            format = "other";
            dontBuild = true;
            nativeBuildInputs = [ pkgs.makeWrapper ];
            propagatedBuildInputs = with py.pkgs; [ inkex lxml tinycss2 pyyaml typer ];
            installPhase = ''
              mkdir -p $out/${py.sitePackages}
              cp -r ica_utils $out/${py.sitePackages}/
              cp ica_cli.py default-config.yaml $out/${py.sitePackages}/

              mkdir -p $out/bin
              cat > $out/bin/ica <<EOF
              #!${py.interpreter}
              from ica_cli import app
              app()
              EOF
              chmod +x $out/bin/ica

              # setup needs these tools at runtime; symbol build toolchain +
              # templates are located via env vars (built symbols are never shipped).
              wrapProgram $out/bin/ica \
                --prefix PATH : ${pkgs.lib.makeBinPath [ pkgs.bash pkgs.git pkgs.rsync pkgs.unzip pkgs.curl py ]} \
                --set ICA_SYMBOL_BUILD_DIR ${symbolBuildDir} \
                --set ICA_TEMPLATES_DIR ${templatesDir} \
                --prefix PYTHONPATH : $out/${py.sitePackages}
            '';
          };
        in {
          inherit ica;
          default = ica;
        });

      apps = forAllSystems (system: {
        ica = {
          type = "app";
          program = "${self.packages.${system}.ica}/bin/ica";
        };
        default = self.apps.${system}.ica;
      });

      devShells = forAllSystems (system:
        let
          pkgs = pkgsFor system;
          pythonEnv = pkgs.python3.withPackages (ps: with ps; [
            inkex
            lxml
            numpy
            pillow
            pyyaml
            tinycss2
            typer
          ]);
        in {
          default = pkgs.mkShell {
            buildInputs = [
              pythonEnv
              cloudia-reader-aws.packages.${system}.default
            ];

            shellHook = ''
              export PATH="${pythonEnv}/bin:$PATH"
              unset PYTHONPATH
              echo "Inkscape Cloud Architect development environment"
              echo "Python with inkex module is available"
            '';
          };
        });
    };
}
