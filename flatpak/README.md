# How to try it out with Flatpak

1. Install Flatpak and Flatpak-Builder
2. Install org.freedesktop.Platform and org.freedesktop.Sdk
3. Clone this repo or download file: io.github.snux.yml
4. Run: flatpak-builder --user --install builddir io.github.snux.yml
5. Command above will create buildir next to your .yml file and it will install snux locally.
6. Run: flatpak run io.github.snux
