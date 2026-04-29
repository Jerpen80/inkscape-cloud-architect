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
