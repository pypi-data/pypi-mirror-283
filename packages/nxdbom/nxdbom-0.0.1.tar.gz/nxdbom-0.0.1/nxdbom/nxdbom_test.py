# Copyright (C) 2023  Nexedi SA and Contributors.
#                     Started by Kirill Smelkov <kirr@nexedi.com>
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.


import nxdbom
import pytest

import os
from os.path import dirname, exists


@pytest.mark.parametrize('url,nameok,verok', [
    ('http://www.python.org/ftp/python/2.7.18/Python-2.7.18.tar.xz',  'Python',  '2.7.18'),
    ('http://www.ijg.org/files/jpegsrc.v9d.tar.gz',                   'jpegsrc', '9d'),
    ('https://github.com/nghttp2/nghttp2/archive/v1.40.0.tar.gz',     'nghttp2', '1.40.0'),
    ('https://golang.org/dl/go1.18.9.src',                            'go',      '1.18.9'),
    ('https://go.dev/dl/go1.20.6.src.tar.gz',                         'go',      '1.20.6'),
    ('https://github.com/tesseract-ocr/tesseract/archive/refs/tags/4.1.1.tar.gz',  'tesseract', '4.1.1'),
    ('https://github.com/tesseract-ocr/tessdata/raw/590567f20dc044f6948a8e2c61afc714c360ad0e/eng.traineddata', 'tessdata', '590567f20dc044f6948a8e2c61afc714c360ad0e/eng.traineddata'),
    ('https://raw.githubusercontent.com/zuphilip/ocropy-models/master/en-default.pyrnn.gz',  'ocropy-models', 'master'),
    ('https://sourceforge.net/projects/swig/files/swig/swig-3.0.12/swig-3.0.12.tar.gz/download',  'swig', '3.0.12'),
    ('https://git.savannah.gnu.org/gitweb/?p=config.git;a=snapshot;h=5e531d39;sf=tgz',  'config', '5e531d39'),
    ('https://lab.nexedi.com/nexedi/wendelin.core.git',  'wendelin.core', None),
    ('/ROOT/develop-eggs/mysqlclient-1.3.12-py2.7-linux-x86_64.egg',  'mysqlclient', '1.3.12'),
    ('https://osdn.net/frs/redir.php?f=ipafonts%2F57330%2FIPAexfont00201.zip', 'IPAexfont', '00201'),
    ('https://osdn.net/frs/redir.php?f=ipafonts%2F51868%2FIPAfont00303.zip',   'IPAfont',   '00303'),
    ('https://osdn.net/frs/redir.php?f=tsukurimashou%2F56948%2Focr-0.2.zip',   'ocr',       '0.2'),
    ('http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz', 'GeoLite2-Country', None),
    ('http://downloadarchive.documentfoundation.org/libreoffice/old/5.2.4.2/rpm/x86_64/LibreOffice_5.2.4.2_Linux_x86-64_rpm.tar.gz',  'LibreOffice', '5.2.4.2'),
    ('http://www.cups.org/software/1.7.4/cups-1.7.4-source.tar.bz2',  'cups', '1.7.4'),
    ('https://github.com/unicode-org/icu/releases/download/release-58-2/icu4c-58_2-src.tgz',  'icu4c', '58_2'),
    ('https://github.com/mozilla/geckodriver/releases/download/v0.16.1/geckodriver-v0.16.1-linux64.tar.gz', 'geckodriver', '0.16.1'),
    ('https://github.com/libevent/libevent/releases/download/release-2.1.11-stable/libevent-2.1.11-stable.tar.gz', 'libevent', '2.1.11'),
    ('https://lab.nexedi.com/bk/onlyoffice_core/repository/archive.tar.bz2?ref=8a40eb47bd80a40ecde14c223525b21852d2fc9f',  'onlyoffice_core', '8a40eb47bd80a40ecde14c223525b21852d2fc9f'),
    ('http://snowball.tartarus.org/dist/libstemmer_c.tgz',  'libstemmer_c', None),
    ('https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.0-patch1/src/hdf5-1.10.0-patch1.tar.bz2',  'hdf5', '1.10.0-patch1'),
    ('http://ftp.debian.org/debian/pool/main/f/findutils/findutils_4.8.0.orig.tar.xz', 'findutils', '4.8.0'),
    ('strict_rfc3339-0.7-py2.7.egg',  'strict_rfc3339', '0.7'),
    ('http://archive.debian.org/debian-archive/debian/pool/main/m/make-dfsg/make-dfsg_3.81.orig.tar.gz', 'make-dfsg', '3.81'),
    ('https://archive.debian.org/debian-archive/debian/pool/main/f/fonts-ocr-b/fonts-ocr-b_0.2~dfsg1.orig.tar.gz', 'fonts-ocr-b', '0.2~dfsg1'),
    ('https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip', 'chromedriver', '2.41'),
    ('https://chromedriver.storage.googleapis.com/91.0.4472.101/chromedriver_linux64.zip', 'chromedriver', '91.0.4472.101'),
    ('https://selenium-release.storage.googleapis.com/3.14/selenium-server-standalone-3.14.0.jar', 'selenium-server-standalone', '3.14'),
    ('https://downloads.metabase.com/v0.48.2/metabase.jar', 'metabase', '0.48.2'),
    ('https://cdimage.debian.org/cdimage/archive/11.7.0/amd64/iso-cd/debian-11.7.0-amd64-netinst.iso', 'debian', '11.7.0'),
    ('https://nodejs.org/dist/v16.19.0/node-v16.19.0.tar.gz', 'nodejs', '16.19.0'),
    ('https://nodejs.org/download/release/v16.19.0/node-v16.19.0-headers.tar.gz', 'node-v16.19.0-headers', '16.19.0'),  # XXX not perfect
    ('https://github.com/nextcloud/news/releases/download/24.0.0/news.tar.gz', 'nextcloud/news', '24.0.0', ),
    ('https://snappymail.eu/repository/nextcloud/snappymail-2.29.4-nextcloud.tar.gz', 'nextcloud/snappymail', '2.29.4'),
    ('https://dlcdn.apache.org/ant/binaries/apache-ant-1.9.16-bin.tar.bz2', 'apache-ant', '1.9.16'),
    ('https://inkscape.org/gallery/item/13330/inkscape-0.92.4_A6N0YOn.tar.bz2', 'inkscape', '0.92.4'),
    ('https://lab.nexedi.com/nexedi/userhosts/repository/a05fe5a3a5cb7005351ef4ec41460089f3ce4d0a/archive.tar.gz', 'userhosts', 'a05fe5a3a5cb7005351ef4ec41460089f3ce4d0a'),
])
def test_namever(url, nameok, verok):
    assert nxdbom.namever(url) == (nameok, verok)

@pytest.mark.parametrize('url', [
    'xxx.conf.in',
    'xxx.cfg',
    'xxx.cfg.in',
    'xxx.cnf.in',
    'xxx.py.in',
    'xxx.sh.in',
    'xxx.yaml.in',
    'xxx.xml.in',
    'xxx.cfg.jinja2',
    'xxx.cfg.jinja2.in',
    'xxx/instance-theia.cfg.jinja.in',
    'xxx.jinja2.cfg',
    'xxx.jinja2.library',
    'xxx.asn',
    'xxx/ltelogs.jinja2.sh',
    'xxx/templates/wrapper.in',
    'xxx/logrotate_entry.in',
    'xxx/matplotlibrc.in',
    'xxx/goenv.sh.in',
    'xxx/promise/yyy',
    'xxx/template-fonts-conf',
    'xxx/template-tomcat-service.sh.in',
    'xxx/server.xml.in',
    'xxx/gitlab-export.in',
    'xxx/watcher.in',
    'xxx/runTestSuite.in',
    'xxx/template-crontab-line.in',
])
def test_isconf(url):
    assert nxdbom.isconf(url) == True


# ---- BOM software ----

testv = []  # of (build, bomok)
def case1(build, bomok):
    testv.append((build, bomok))

case1("""\
[ncurses]
recipe = slapos.recipe.cmmi
url = http://ftp.gnu.org/gnu/ncurses/ncurses-6.2.tar.gz
""", """\
ncurses                      6.2        http://ftp.gnu.org/gnu/ncurses/ncurses-6.2.tar.gz
""")

case1("""\
[neoppod-repository.git]
recipe = slapos.recipe.build:gitclone
repository = https://lab.nexedi.com/nexedi/neoppod.git
""", """
>>> gits:
neoppod                      HEAD       https://lab.nexedi.com/nexedi/neoppod.git
""")

case1("""\
[neoppod-repository]
recipe = slapos.recipe.build:gitclone
repository = https://lab.nexedi.com/nexedi/neoppod
""", """
>>> gits:
neoppod                      HEAD       https://lab.nexedi.com/nexedi/neoppod
""")

case1("""\
[neoppod-repository-github]
recipe = slapos.recipe.build:gitclone
repository = https://github.com/nexedi/neoppod
""", """
>>> gits:
neoppod                      HEAD       https://github.com/nexedi/neoppod
""")

case1("""\
[secret-repository.git]
recipe = slapos.recipe.build:gitclone
repository = https://login:password@lab.nexedi.com/nexedi/secret.git
""", """
>>> gits:
secret                       HEAD       https://lab.nexedi.com/nexedi/secret.git
""")

case1("""\
[ocropy-eng-traineddata]
recipe = slapos.recipe.build:download
url = https://raw.githubusercontent.com/zuphilip/ocropy-models/master/en-default.pyrnn.gz
""", """\
ocropy-models                master     https://raw.githubusercontent.com/zuphilip/ocropy-models/master/en-default.pyrnn.gz
""")

# legacy hexagonit.recipe.download recipe
case1("""\
[ocropy-eng-traineddata]
download-only = true
recipe = hexagonit.recipe.download
url = https://raw.githubusercontent.com/zuphilip/ocropy-models/master/en-default.pyrnn.gz
""", """\
ocropy-models                master     https://raw.githubusercontent.com/zuphilip/ocropy-models/master/en-default.pyrnn.gz
""")

case1("""\
[scons]
recipe = slapos.recipe.build:download-unpacked
url = https://prdownloads.sourceforge.net/scons/scons-local-2.3.0.tar.gz
""", """\
scons-local                  2.3.0      https://prdownloads.sourceforge.net/scons/scons-local-2.3.0.tar.gz
""")

case1("""\
[ipaex-fonts]
recipe = slapos.recipe.build:download-unpacked
url = https://osdn.net/frs/redir.php?f=ipafonts%2F57330%2FIPAexfont00201.zip
""", """\
IPAexfont                    00201      https://osdn.net/frs/redir.php?f=ipafonts%2F57330%2FIPAexfont00201.zip
""")

# download from local filesystem - ignore if that file comes from the profile itself
case1("""\
[mariadb-resiliency-after-import-script]
recipe = slapos.recipe.build:download
url = /BASE/stack/erp5/instance-mariadb-resiliency-after-import-script.sh.in
_profile_base_location_ = /BASE
""", '')

# slapos.build.:download with hash in the url
case1("""\
[geolite2-country]
recipe = slapos.recipe.build:download-unpacked
url = http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz#dc6224c648350d90f344a0c5c3ca5474
""", """\
GeoLite2-Country             dc6224c6   http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz
""")

# slapos.recipe.build from a git clone
case1("""\
[shellinabox-repository]
recipe = slapos.recipe.build:gitclone
repository = https://github.com/shellinabox/shellinabox
revision = b8285748993c4c99e80793775f3d2a0a4e962d5a

[shellinabox]
recipe = slapos.recipe.cmmi
path = ${shellinabox-repository:location}
""", """
>>> gits:
shellinabox                  b8285748993c4c99e80793775f3d2a0a4e962d5a https://github.com/shellinabox/shellinabox
""")

for x in ('gcc', 'python', 'ZODB', 'ZEO', 'tempstorage', 'generic_testrunner_init'):
    case1("""\
[%s]
recipe = slapos.recipe.build
""" % x, '')    # empty

case1("""\
[without-url]
recipe = slapos.recipe.build
init = do something
""",
''
)

case1("""\
[without-url]
recipe = slapos.recipe.build
install = install from path
path = somewhere
""",
''
)

# wrapper scripts generated by slapos.recipe.build (firefox-wrapper-*
# chromium-wrapper-* )
case1("""\
[wrapper-script]
recipe = slapos.recipe.build
install = ( create a wrapper from another part )
location = /ROOT/bin/executable
-- /ROOT/bin/executable --
""", '')

case1("""\
[without-url]
recipe = slapos.recipe.build
install =
    some_python_that_we_cannot_introspect()
location = somewhere
""",
''
)

case1("""\
[url-detection]
recipe = slapos.recipe.build
xxx-url = https://lab.nexedi.com/...
location = somewhere
""",
NotImplementedError('url-detection might be using url with slapos.recipe.build in an unsupported way')
)

case1("""\
[url-detection]
recipe = slapos.recipe.build
xxx = interpqolation %s  # this should not confuse the detection of urls
location = somewhere
""",
''
)

case1("""\
[template-logrotate-base]
recipe = slapos.recipe.template:jinja2
url = /srv/slapgrid/slappart47/srv/project/slapos/stack/logrotate/instance-logrotate-base.cfg.in
""", '')    # config ignored

case1("""\
[cfg-environment]
recipe = collective.recipe.template
input = inline: zzz
""", '')    # inline ignore

# legacy options (template & rendered) for slapos.recipe.template
case1("""\
[matplotlibrc]
recipe = slapos.recipe.template:jinja2
rendered = /ROOT/parts/matplotlibrc/matplotlibrc
template = https://lab.nexedi.com/nexedi/slapos/raw/1.0.167.10/component/matplotlib/matplotlibrc.in
""", '')

case1("""\
[randomsleep]
recipe = slapos.recipe.template:jinja2
template = inline:x
""", '')

case1("""\
[randomsleep]
recipe = slapos.recipe.template
template = inline:x
""", '')

# slapos.recipe.template < 5 removed url from options
case1("""\
[template-fonts-conf]
recipe = slapos.recipe.template
__buildout_signature__ = Jinja2-2.9.5 MarkupSafe-1.0 setuptools-44.0.0 six-1.12.0 slapos.recipe.template-4.4 zc.buildout-2.7.1+slapos009 gcc:f7deef0474b0074beef57c09c3a00152
filename = fonts.conf.in
md5sum = 6967e553630d107fc0a59b14de8b0251
mode = 640
output = /srv/slapgrid/slappart15/srv/runner/instance/slappart7/tmp/soft/401a9f2389413c4c542be71a6c8a3a39/parts/template-fonts-conf
""", '')

case1("""\
[neoppod-develop]
recipe = zc.recipe.egg:develop
__buildout_installed__ = /ROOT/develop-eggs/neoppod.egg-link
""", '')    # .egg-link ignored

case1("""\
[python-mysqlclient]
recipe = zc.recipe.egg:custom
__buildout_installed__ = /ROOT/develop-eggs/mysqlclient-1.3.12-py2.7-linux-x86_64.egg
""", """
>>> eggs:
mysqlclient                  1.3.12     https://pypi.org/project/mysqlclient/1.3.12/
""")

case1("""\
[slapos-toolbox-dependencies]
recipe = zc.recipe.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs = lxml
        pycurl
        Mako
-- /ROOT/develop-eggs/lxml-4.9.1-py2.7-linux-x86_64.egg/x --
-- /ROOT/develop-eggs/pycurl-7.43.0-py2.7-linux-x86_64.egg/x --
-- /ROOT/eggs/Mako-1.1.4-py2.7.egg/x --
""", """
>>> eggs:
lxml                         4.9.1      https://pypi.org/project/lxml/4.9.1/
Mako                         1.1.4      https://pypi.org/project/Mako/1.1.4/
pycurl                       7.43.0     https://pypi.org/project/pycurl/7.43.0/
""")

case1("""\
[ZODB5]
recipe = zc.recipe.egg:eggs
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs = ZODB
      BTrees
-- /ROOT/eggs/ZODB-5.8.0-py2.7.egg/x --
-- /ROOT/develop-eggs/BTrees-4.11.3-py2.7-linux-x86_64.egg/x --
""", """
>>> eggs:
BTrees                       4.11.3     https://pypi.org/project/BTrees/4.11.3/
ZODB                         5.8.0      https://pypi.org/project/ZODB/5.8.0/
""")

case1("""\
[erp5-python-interpreter]
recipe = zc.recipe.egg:scripts
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs = pygolang
        neoppod[admin, ctl, master]
-- /ROOT/develop-eggs/pygolang-0.1-py2.7-linux-x86_64.egg/x --
-- /ROOT/develop-eggs/neoppod.egg-link --
""", """
>>> eggs:
pygolang                     0.1        https://pypi.org/project/pygolang/0.1/
""")

case1("""\
[manpy]
recipe = zc.recipe.egg:script
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs = dream
initialization = # pulp needs glpk in $PATH
	import os
	os.environ['PATH'] = '...'
-- /ROOT/develop-eggs/dream.egg-link --
""", '')


# no `eggs =`
case1("""\
[selenium]
recipe = zc.recipe.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
-- /ROOT/eggs/selenium-3.141.0-py2.7.egg/x --
""", """
>>> eggs:
selenium                     3.141.0    https://pypi.org/project/selenium/3.141.0/
""")

# msgpack as egg and as c library at the same time
case1("""
[messagepack]
recipe = slapos.recipe.cmmi
url = http://downloads.sourceforge.net/project/msgpack/msgpack/cpp/msgpack-0.5.4.tar.gz

[msgpack-python]
recipe = zc.recipe.egg:custom
__buildout_installed__ = /ROOT/develop-eggs/msgpack-0.6.2-py2.7-linux-x86_64.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
egg = msgpack
""", """\
msgpack                      0.5.4      http://downloads.sourceforge.net/project/msgpack/msgpack/cpp/msgpack-0.5.4.tar.gz

>>> eggs:
msgpack                      0.6.2      https://pypi.org/project/msgpack/0.6.2/
""")

# %(__buildout_space_...) in egg can be read
case1("""\
[zzz]
recipe = zc.recipe.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs =
    aaa
    bbb%(__buildout_space_n__)s
-- /ROOT/eggs/aaa-1.2.3.egg/x --
-- /ROOT/eggs/bbb-5.6.7.egg/x --
""", """
>>> eggs:
aaa                          1.2.3      https://pypi.org/project/aaa/1.2.3/
bbb                          5.6.7      https://pypi.org/project/bbb/5.6.7/
""")

# +slapospatchedXXX is removed from egg URL
case1("""\
[astroid]
recipe = zc.recipe.egg:custom
__buildout_installed__ = /ROOT/develop-eggs/astroid-1.3.8+slapospatched001-py2.7.egg
""", """
>>> eggs:
astroid                      1.3.8+slapospatched001 https://pypi.org/project/astroid/1.3.8/
""")

# nxd or slaposXXX in egg version -> nexedi.org
case1("""\
[testrunner]
recipe = zc.recipe.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs = SOAPpy
       zc.recipe.egg
       zc.buildout
-- /ROOT/eggs/SOAPpy-0.12.0nxd001-py2.7.egg/x --
-- /ROOT/eggs/zc.buildout-2.7.1+slapos019-py3.7.egg/x --
-- /ROOT/eggs/zc.recipe.egg-2.0.3+slapos003-py2.7.egg/x --
""", """
>>> eggs:
SOAPpy                       0.12.0nxd001 http://www.nexedi.org/static/packages/source/SOAPpy-0.12.0nxd001.tar.gz
zc.buildout                  2.7.1+slapos019 http://www.nexedi.org/static/packages/source/slapos.buildout/zc.buildout-2.7.1+slapos019.tar.gz
zc.recipe.egg                2.0.3+slapos003 http://www.nexedi.org/static/packages/source/zc.recipe.egg-2.0.3+slapos003.tar.gz
""")

# %20 in URL
case1("""\
[zabbix-agent]
recipe = slapos.recipe.cmmi
url = http://downloads.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/2.0.10/zabbix-2.0.10.tar.gz
""", """\
zabbix                       2.0.10     http://downloads.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/2.0.10/zabbix-2.0.10.tar.gz
""")

# plone.recipe.command is ignored
case1("""\
[gowork.dir]
recipe = plone.recipe.command
""", '')
# also this variation from some test profiles
case1("""\
[gowork.dir]
recipe = plone.recipe.command==1.1
""", '')

# zc.recipe.testrunner is ignored
case1("""\
[dream-testrunner]
recipe = zc.recipe.testrunner
eggs = dream
""", '')

# ruby gems
case1("""\
[gems]
recipe = rubygemsrecipe
location = /ROOT/parts/gems
-- /ROOT/parts/gems/lib/ruby/gems/specifications/gitlab-puma-4.3.3.gitlab.2.gemspec --
# -*- encoding: utf-8 -*-
# stub: gitlab-puma 4.3.3.gitlab.2 ruby lib
# stub: ext/puma_http11/extconf.rb
-- /ROOT/parts/gems/lib/ruby/gems/specifications/pyu-ruby-sasl-0.0.3.3.gemspec --
# -*- encoding: utf-8 -*-
# stub: pyu-ruby-sasl 0.0.3.3 ruby lib
-- /ROOT/parts/gems/lib/ruby/gems/specifications/toml-rb-1.0.0.gemspec --
# -*- encoding: utf-8 -*-
# stub: toml-rb 1.0.0 ruby lib
-- /ROOT/parts/gems/lib/ruby/gems/specifications/tzinfo-1.2.6.gemspec --
# -*- encoding: utf-8 -*-
# stub: tzinfo 1.2.6 ruby lib
-- /ROOT/parts/gems/lib/ruby/gems/specifications/google-protobuf-3.8.0-x86_64-linux.gemspec --
# -*- encoding: utf-8 -*-
# stub: google-protobuf 3.8.0 x86_64-linux lib
-- /ROOT/parts/gems/lib/ruby/gems/specifications/apollo_upload_server-2.0.0.beta.3.gemspec --
# -*- encoding: utf-8 -*-
# stub: apollo_upload_server 2.0.0.beta.3 ruby lib
-- /ROOT/parts/gems/lib/ruby/gems/specifications/omniauth-gitlab-1.0.3.gemspec --
# -*- encoding: utf-8 -*-
# stub: omniauth-gitlab 1.0.3 ruby lib
-- /ROOT/parts/gems/lib/ruby/gems/specifications/diff_match_patch-0.1.0.gemspec --
# -*- encoding: utf-8 -*-
# stub: diff_match_patch 0.1.0 ruby lib

""", """
>>> gems:
apollo_upload_server         2.0.0.beta.3 https://rubygems.org/gems/apollo_upload_server/versions/2.0.0.beta.3
diff_match_patch             0.1.0      https://rubygems.org/gems/diff_match_patch/versions/0.1.0
gitlab-puma                  4.3.3.gitlab.2 https://rubygems.org/gems/gitlab-puma/versions/4.3.3.gitlab.2
google-protobuf              3.8.0      https://rubygems.org/gems/google-protobuf/versions/3.8.0
omniauth-gitlab              1.0.3      https://rubygems.org/gems/omniauth-gitlab/versions/1.0.3
pyu-ruby-sasl                0.0.3.3    https://rubygems.org/gems/pyu-ruby-sasl/versions/0.0.3.3
toml-rb                      1.0.0      https://rubygems.org/gems/toml-rb/versions/1.0.0
tzinfo                       1.2.6      https://rubygems.org/gems/tzinfo/versions/1.2.6
""")

# readline 8 and 5 used simultaneously    ->  older one is presented as readline5
# libpng   12 and 16 used simultaneously  ->  ----//----                libpng12
# ----/---- Python2 and Python3
case1("""\
[readline]
recipe = slapos.recipe.cmmi
url = http://ftp.gnu.org/gnu/readline/readline-8.1.tar.gz
[readline5]
recipe = slapos.recipe.cmmi
url = http://ftp.gnu.org/gnu/readline/readline-5.2.tar.gz

[libpng]
recipe = slapos.recipe.cmmi
url = http://download.sourceforge.net/libpng/libpng-1.6.37.tar.xz
[libpng12]
recipe = slapos.recipe.cmmi
url = http://download.sourceforge.net/libpng/libpng-1.2.59.tar.xz

[python2.7]
recipe = slapos.recipe.cmmi
url = http://www.python.org/ftp/python/2.7.18/Python-2.7.18.tar.xz
[python3]
recipe = slapos.recipe.cmmi
url = https://www.python.org/ftp/python/3.9.15/Python-3.9.15.tar.xz
""", """\
libpng                       1.6.37     http://download.sourceforge.net/libpng/libpng-1.6.37.tar.xz
libpng12                     1.2.59     http://download.sourceforge.net/libpng/libpng-1.2.59.tar.xz
Python                       2.7.18     http://www.python.org/ftp/python/2.7.18/Python-2.7.18.tar.xz
Python3                      3.9.15     https://www.python.org/ftp/python/3.9.15/Python-3.9.15.tar.xz
readline                     8.1        http://ftp.gnu.org/gnu/readline/readline-8.1.tar.gz
readline5                    5.2        http://ftp.gnu.org/gnu/readline/readline-5.2.tar.gz
""")

# egg directoty on the filesystem might have different case and _ instead of -
case1("""\
[cython-zstd]
recipe = zc.recipe.egg:custom
egg = cython-zstd
__buildout_installed__ = /ROOT/develop-eggs/cython_zstd-0.2-py2.7-linux-x86_64.egg

[cython]
recipe = zc.recipe.egg:custom
egg = cython
__buildout_installed__ = /Root/develop-eggs/Cython-0.29.24-py2.7-linux-x86_64.egg

[neoppod]
recipe = zc.recipe.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs = cython-zstd
       cython
-- /ROOT/develop-eggs/cython_zstd-0.2-py2.7-linux-x86_64.egg/x --
-- /ROOT/develop-eggs/Cython-0.29.24-py2.7-linux-x86_64.egg/x --
""", """
>>> eggs:
Cython                       0.29.24    https://pypi.org/project/Cython/0.29.24/
cython_zstd                  0.2        https://pypi.org/project/cython_zstd/0.2/
""")

# py3 eggs
case1("""\
[xxx]
recipe = zc.recipe.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs = aaa
       bbb
       ccc
-- /ROOT/eggs/aaa-1.2-py3.7.egg/x --
-- /ROOT/eggs/bbb-3.4-py3.8.egg/x --
-- /ROOT/develop-eggs/ccc-5.6.7-py3.9-linux-x86_64.egg/x --
""", """
>>> eggs:
aaa                          1.2        https://pypi.org/project/aaa/1.2/
bbb                          3.4        https://pypi.org/project/bbb/3.4/
ccc                          5.6.7      https://pypi.org/project/ccc/5.6.7/
""")

# multiple eggs are rejected
# TODO try to improve zc.recipe.egg to emit information into .installed.cfg instead of us scanning the filesystem
case1("""
[ccc]
recipe = zc.recipe.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs = setuptools
-- /ROOT/eggs/setuptools-44.1.1-py3.7.egg --
-- /ROOT/eggs/setuptools-44.1.1-py3.9.egg --
""",
ValueError("egg setuptools is present multiple times: ['setuptools-44.1.1-py3.7.egg', 'setuptools-44.1.1-py3.9.egg']"))

# eggs installed indirectly are also reported
case1("""
[eggs]
recipe = zc.recipe.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
eggs = Zope
__buildout_installed__ = /ROOT/bin/runwsgi
-- /ROOT/eggs/Zope-4.8.7-py2.7.egg/x --
-- /ROOT/bin/runwsgi --
#!/ROOT/bin/python2.7

import sys
sys.path[0:0] = [
  '/ROOT/part/neoppod-repository',
  '/ROOT/eggs/Zope-4.8.7-py2.7.egg',
  '/ROOT/eggs/certifi-2020.4.5.1-py2.7.egg',
  ]

...
""", """
>>> eggs:
certifi                      2020.4.5.1 https://pypi.org/project/certifi/2020.4.5.1/
Zope                         4.8.7      https://pypi.org/project/Zope/4.8.7/
""")

# libreoffice
case1("""\
[libreoffice-bin]
recipe = slapos.recipe.build
url = http://downloadarchive.documentfoundation.org/libreoffice/old/5.2.4.2/rpm/x86_64/LibreOffice_5.2.4.2_Linux_x86-64_rpm.tar.gz
""", """\
LibreOffice                  5.2.4.2    http://downloadarchive.documentfoundation.org/libreoffice/old/5.2.4.2/rpm/x86_64/LibreOffice_5.2.4.2_Linux_x86-64_rpm.tar.gz
""")

# libstemmer_c comes without version
case1("""\
[libstemmer]
recipe = slapos.recipe.cmmi
url = http://snowball.tartarus.org/dist/libstemmer_c.tgz
""", """\
libstemmer_c                            http://snowball.tartarus.org/dist/libstemmer_c.tgz
""")

# two different versions of the same software are ok
case1("""\
[scons-0]
recipe = slapos.recipe.build:download-unpacked
url = https://prdownloads.sourceforge.net/scons/scons-local-2.3.0.tar.gz

[scons-1]
recipe = slapos.recipe.build:download-unpacked
url = https://prdownloads.sourceforge.net/scons/scons-local-2.3.1.tar.gz
""", """\
scons-local                  2.3.0      https://prdownloads.sourceforge.net/scons/scons-local-2.3.0.tar.gz
scons-local                  2.3.1      https://prdownloads.sourceforge.net/scons/scons-local-2.3.1.tar.gz
""")

# edge case: tesseract from old ( 1.0.167.10 ) ERP5 software release
case1("""\
[tesseract-eng-traineddata]
md5sum = 57e0df3d84fed9fbf8c7a8e589f8f012
recipe = slapos.recipe.build:download
url = https://github.com/tesseract-ocr/tessdata/raw/590567f20dc044f6948a8e2c61afc714c360ad0e/eng.traineddata

[tesseract-osd-traineddata]
md5sum = 7611737524efd1ce2dde67eff629bbcf
recipe = slapos.recipe.build:download
url = https://github.com/tesseract-ocr/tessdata/raw/590567f20dc044f6948a8e2c61afc714c360ad0e/osd.traineddata
""",
"""\
tessdata                     590567f20dc044f6948a8e2c61afc714c360ad0e/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/590567f20dc044f6948a8e2c61afc714c360ad0e/eng.traineddata
tessdata                     590567f20dc044f6948a8e2c61afc714c360ad0e/osd.traineddata https://github.com/tesseract-ocr/tessdata/raw/590567f20dc044f6948a8e2c61afc714c360ad0e/osd.traineddata
""")


def populate_software_directory_from_build(tmpdir, build):
    build = '-- /ROOT/.installed.cfg --\n' + build
    build = build.replace('/ROOT', str(tmpdir))
    build = build.replace('/BASE', str(tmpdir / 'base'))
    ar = txtar_parse(build)
    assert ar.comment == ''
    for f, data in ar.files.items():
        assert f.startswith(str(tmpdir))
        os.makedirs(dirname(f), exist_ok=True)
        with open(f, 'w') as _:
            _.write(data)
    buildout_cfg = (tmpdir / 'buildout.cfg')
    if not buildout_cfg.exists():
        buildout_cfg.write_text('''
[buildout]
extends = https://slapos.example.invalid/software/example/software.cfg
''',
'utf-8')


@pytest.mark.parametrize('build,bomok', testv)
def test_bom_software(tmpdir, build, bomok):
    populate_software_directory_from_build(tmpdir, build)
    bom = {}
    if isinstance(bomok, Exception):
        with pytest.raises(type(bomok)) as e:
            nxdbom.bom_software(tmpdir)
        assert str(e.value) == str(bomok)
    else:
        bom = nxdbom.bom_software(tmpdir)
        assert nxdbom.fmt_bom(bom) == bomok
    assert nxdbom.fmt_bom_cyclonedx_json(bom, str(tmpdir))


def test_bom_cyclonedx_json(tmpdir):
    build = """\
[libpng]
recipe = slapos.recipe.cmmi
url = http://download.sourceforge.net/libpng/libpng-1.6.37.tar.xz

[erp5]
recipe = slapos.recipe.build:gitclone
repository = https://lab.nexedi.com/nexedi/erp5
revision = 1234abcd

[snappy]
recipe = slapos.recipe.cmmi
url = https://github.com/google/snappy/archive/1.1.8.tar.gz

[eggs]
recipe = zc.recipe.egg
_d = /ROOT/develop-eggs
_e = /ROOT/eggs
__buildout_installed__ =
eggs =
    aaa
-- /ROOT/eggs/aaa-1.2.3.egg/x --
"""
    populate_software_directory_from_build(tmpdir, build)
    bom = nxdbom.bom_software(tmpdir)
    cyclonedx = nxdbom.fmt_bom_cyclonedx_json(bom, tmpdir)
    assert cyclonedx['bomFormat'] == 'CycloneDX'
    assert cyclonedx['specVersion'] == '1.5'
    assert cyclonedx['serialNumber']
    assert cyclonedx['metadata']['timestamp']
    assert cyclonedx['metadata']['component']['name'] == 'example'
    assert cyclonedx['metadata']['component']['externalReferences'] == [
        {
            "type": "build-meta",
            "url": "https://slapos.example.invalid/software/example/software.cfg"
        }
    ]
    assert [c['name'] for c in cyclonedx['metadata']['tools']['components']] == ['nxdbom']
    assert cyclonedx['components'] == [
         {
             'externalReferences': [
                 {
                     'type': 'distribution',
                     'url': 'https://pypi.org/project/aaa/1.2.3/',
                 },
             ],
             'name': 'aaa',
             'purl': 'pkg:pypi/aaa@1.2.3',
             'type': 'library',
             'version': '1.2.3',
         },
         {
             'name': 'erp5',
             'purl': 'pkg:generic/erp5@1234abcd',
             'type': 'library',
             'version': '1234abcd',
             'cpe': 'cpe:2.3:*:*:erp5:1234abcd:*:*:*:*:*:*:*',
             'externalReferences': [
                 {'url': 'https://lab.nexedi.com/nexedi/erp5', 'type': 'vcs'}
             ],
         },
         {
             'cpe': 'cpe:2.3:*:*:libpng:1.6.37:*:*:*:*:*:*:*',
             'externalReferences': [
                 {
                     'type': 'distribution',
                     'url': 'http://download.sourceforge.net/libpng/libpng-1.6.37.tar.xz',
                 },
             ],
             'name': 'libpng',
             'purl': 'pkg:generic/libpng@1.6.37',
             'type': 'library',
             'version': '1.6.37',
         },
         {
             'name': 'snappy',
             'purl': 'pkg:generic/snappy@1.1.8',
             'type': 'library',
             'version': '1.1.8',
             'cpe': 'cpe:2.3:*:google:snappy:1.1.8:*:*:*:*:*:*:*',
             'externalReferences': [
                 {
                     'url': 'https://github.com/google/snappy/archive/1.1.8.tar.gz',
                     'type': 'distribution',
                 }
             ],
         },
     ]


# loading non-existing .installed.cfg -> error
def test_bom_software_eexist():
    ne = '/nonexisting'
    assert not exists(ne)
    with pytest.raises(RuntimeError, match="Cannot load '%s/.installed.cfg'" % ne):
        nxdbom.bom_software(ne)


# ---- txtar ----

# txtar_* provide support for archives in txtar format
# https://pkg.go.dev/golang.org/x/tools/txtar#hdr-Txtar_format
class txtar_Archive:
    # .comment  str
    # .files    {}  name -> text
    pass

def txtar_parse(text): # -> txtar_Archive
    comment = ''
    files = {}
    current_file = None # current file | None for comments
    current_text = ''   # accumulator for text of current file
    def flush(next_file):
        nonlocal comment, current_file, current_text
        if current_file is None:
            comment = current_text
        else:
            files[current_file] = current_text

        current_text = ''
        current_file = next_file

    for l in text.splitlines(keepends=True):
        if not l.endswith('\n'):
            l += '\n'   # missing trailing newline on the final line

        if l.startswith('-- ') and l.rstrip().endswith(' --'):
            _ = l.rstrip()
            _ = _.removeprefix('-- ')
            _ = _.removesuffix(' --')
            next_file = _.strip()
            flush(next_file)
            continue

        current_text += l

    flush(None)
    ar = txtar_Archive()
    ar.comment = comment
    ar.files   = files
    return ar
