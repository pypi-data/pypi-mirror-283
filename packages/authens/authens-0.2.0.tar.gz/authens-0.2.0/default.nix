{
  sources ? import ./npins,
  pkgs ? import sources.nixpkgs { },
}:

let
  nix-pkgs = import sources.nix-pkgs { inherit pkgs; };

  python3 = pkgs.python3.override { packageOverrides = _: _: { inherit (nix-pkgs) python-cas; }; };

  deploy-pypi = pkgs.writeShellApplication {
    name = "deploy-pypi";

    runtimeInputs = [
      (pkgs.python3.withPackages (ps: [
        ps.setuptools
        ps.build
        ps.twine
      ]))
    ];

    text = ''
      # Clean the repository
      rm -rf dist

      python -m build
      twine upload dist/*
    '';
  };
in

{
  devShell = pkgs.mkShell {
    name = "cas-eleves.dev";

    packages = [
      (python3.withPackages (ps: [
        ps.django
        ps.python-ldap
        ps.python-cas
      ]))

      pkgs.gettext
      pkgs.gtranslator
    ];
  };

  publishShell = pkgs.mkShell {
    name = "loadcredential.publish";

    packages = [ deploy-pypi ];
  };
}
