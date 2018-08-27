with import <nixpkgs> {};
with pkgs.python35Packages;

( let
    visilibity = pkgs.callPackage /home/alli/src/PyVisiLibity/release.nix {
        pkgs = pkgs;
        buildPythonPackage = pkgs.python35Packages.buildPythonPackage;
    };

    in pkgs.python35.withPackages (ps: 
        [ 
        ps.matplotlib 
        ps.networkx 
        ps.pygame
        visilibity
        ])
).env
