with import <nixpkgs> {};

stdenv.mkDerivation rec {
    name = "Coms";
    buildInputs = [python2 python2Packages.scipy];
}
