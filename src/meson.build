pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'decks'
python = import('python')

suite_common = subproject('suite-common')
sc_sources = suite_common.get_variable('suite_common_sources')
install_data(sc_sources, install_dir: pkgdatadir / 'suite_common')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('pkgdatadir', pkgdatadir)
conf.set('localedir', get_option('prefix') / get_option('localedir'))

configure_file(
  input: 'decks.in',
  output: 'decks',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x',
)

install_data(
  [ '__init__.py', 'main.py', 'window.py', 'fileio.py', 'engine.js' ],
  install_dir: moduledir,
)

# Vendored JS engines (MIT: fabric.js, reveal.js), inlined at runtime.
install_data(
  [
    'vendor/fabric.min.js',
    'vendor/reveal.js',
    'vendor/reveal.css',
    'vendor/reveal-theme.css',
  ],
  install_dir: moduledir / 'vendor',
)
