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
        ps.sphinx
        ps.sphinx_rtd_theme
        ps.cycler
        ps.decorator
        #ps.kiwisolver
        ps.matplotlib
        ps.networkx
        ps.numpy
        ps.pyparsing
        #ps.PyQt5
        #ps.PyQt5-sip
        ps.python-dateutil
        ps.six
        visilibity
        ])
).env
