export default {
  logo: <span>ProPresenter Triggers</span>,
  useNextSeoProps() {
    return {
      titleTemplate: "%s – Docs"
    }
  },
  primaryHue: 24,
  project: {
    link: 'https://github.com/mackenly/propresenter-triggers'
  },
  docsRepositoryBase: "https://github.com/mackenly/propresenter-triggers/tree/main/docs",
  head: (
    <>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="description" content="Docs for propresenter-triggers Automation Project" />
      <meta property="og:title" content="ProPresenter Triggers Docs" />
      <meta property="og:description" content="Docs for propresenter-triggers Automation Project" />
      <meta name="msapplication-TileColor" content="#000000" />
      <meta name="theme-color" content="#000000" />
    </>
  ),
  footer: {
    text: (
      <span>
        ©{' '}{new Date().getFullYear()}{' '}
        <a href="https://tricitiesmediagroup.com" target="_blank">
          Tricities Media Group x Mackenly Jones
        </a>
        .
      </span>
    )
  }
  // ...
}