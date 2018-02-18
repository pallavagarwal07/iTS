with import <nixpkgs> {};

stdenv.mkDerivation rec {
    name = "Coms";
    buildInputs = [python3 python3Packages.scipy];
}
