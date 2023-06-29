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