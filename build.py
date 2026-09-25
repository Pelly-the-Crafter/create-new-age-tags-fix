"""Build Create: New Age Tags Fix as both a datapack and a mod jar, into build/.

Usage: python build.py

- build/create-new-age-tags-fix-<version>.zip: the datapack (the datapack/ folder), for a world's datapacks folder.
- build/create-new-age-tags-fix-<version>.jar: the same data as a NeoForge mod, for a mods folder (applies to every world).

The jar's one class is compiled with the Java 21 compiler that Prism Launcher ships, against the NeoForge mod loader jar
Prism downloaded (set PRISM_DIR if Prism lives elsewhere). Both files are written with fixed timestamps, so rebuilding
unchanged sources gives byte-identical files. The version comes from src/main/resources/META-INF/neoforge.mods.toml.
"""
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATAPACK = HERE / "datapack"
OUT = HERE / "build"
PRISM = Path(os.environ.get("PRISM_DIR", Path(os.environ["APPDATA"]) / "PrismLauncher"))
JAVAC = PRISM / "java/java-runtime-delta/bin/javac.exe"
FML = PRISM / "libraries/net/neoforged/fancymodloader/loader/4.0.44/loader-4.0.44.jar"
DIST = PRISM / "libraries/net/neoforged/mergetool/2.0.0/mergetool-2.0.0-api.jar"  # @Mod's Dist enum
FIXED_TIME = (2020, 1, 1, 0, 0, 0)


def add(z, name, data):
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    z.writestr(info, data)


def tree(root):
    return sorted((p.relative_to(root).as_posix(), p.read_bytes()) for p in root.rglob("*") if p.is_file())


def main():
    toml = (HERE / "src/main/resources/META-INF/neoforge.mods.toml").read_text(encoding="utf-8")
    version = re.search(r'^version = "([^"]+)"', toml, re.M).group(1)
    OUT.mkdir(exist_ok=True)

    zip_path = OUT / f"create-new-age-tags-fix-{version}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in tree(DATAPACK):
            add(z, name, data)

    jar_path = OUT / f"create-new-age-tags-fix-{version}.jar"
    with tempfile.TemporaryDirectory() as tmp:
        sources = [str(p) for p in (HERE / "src/main/java").rglob("*.java")]
        subprocess.run([str(JAVAC), "--release", "21", "-proc:none", "-Xlint:-options", "-cp", os.pathsep.join([str(FML), str(DIST)]), "-d", tmp, *sources],
                       check=True)
        with zipfile.ZipFile(jar_path, "w", zipfile.ZIP_DEFLATED) as z:
            add(z, "META-INF/MANIFEST.MF", "Manifest-Version: 1.0\nAutomatic-Module-Name: create_new_age_tags_fix\n")
            for name, data in tree(HERE / "src/main/resources") + tree(Path(tmp)) + tree(DATAPACK):
                add(z, name, data)
    for p in (zip_path, jar_path):
        print(f"built {p.relative_to(HERE)} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
