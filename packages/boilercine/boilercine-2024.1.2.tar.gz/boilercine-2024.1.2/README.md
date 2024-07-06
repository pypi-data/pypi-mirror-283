# boilercine

[![All Contributors](https://img.shields.io/github/all-contributors/softboiler/boilercine?color=ee8449&style=flat-square)](#contributors)

Convert CINEs for a boiling study.

Install the dependencies of this package manually.

```Shell
pip install --no-deps git+https://github.com/ottomatic-io/pycine@815cfca06cafc50745a43b2cd0168982225c6dca
pip install opencv-python  # Or a different flavor of your choice, e.g. `opencv-contrib-python`
pip install git+https://github.com/blakeNaccarato/boilercine@main
```

I did not add pycine explicitly to requirements because this package relies on an unreleased commit of pycine. Install it without its dependencies to avoid forcing installation of a particular flavor of OpenCV. The `opencv-python` package is a good choice for most users, but you could use `opencv-contrib-python` as well. I reproduce all of its other dependencies as the dependencies of this package.

## Project information

- [Changes](<https://softboiler.github.io/boilercine/changelog.html>)
- [Docs](<https://softboiler.github.io/boilercine>)
- [Contributing](<https://softboiler.github.io/boilercine/contributing.html>)

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://www.blakenaccarato.com/"><img src="https://avatars.githubusercontent.com/u/20692450?v=4?s=100" width="100px;" alt="Blake Naccarato"/><br /><sub><b>Blake Naccarato</b></sub></a><br /><a href="#code-blakeNaccarato" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
