(function () {
  const win = window
  const doc = document.documentElement

  doc.classList.remove('no-js')
  doc.classList.add('js')

  // Fix hero background height on desktop
  const heroDesktopBg = document.querySelector('.site-header-large-bg span')

  fixHeroBgHeight()
  win.addEventListener('load', fixHeroBgHeight)
  win.addEventListener('resize', fixHeroBgHeight)

  function fixHeroBgHeight () {
    const bodyHeight = doc.getElementsByTagName('body')[0].clientHeight
    heroDesktopBg.style.height = `${bodyHeight}px`
  }

  // Reveal animations
  if (document.body.classList.contains('has-animations')) {
    /* global ScrollReveal */
    const sr = window.sr = ScrollReveal()

    sr.reveal('.hero-title, .hero-paragraph, .newsletter-form', {
      duration: 1000,
      distance: '40px',
      easing: 'cubic-bezier(0.5, -0.01, 0, 1.005)',
      origin: 'top',
      interval: 150
    })

    sr.reveal('.hero-ball', {
      delay: 1000,
      duration: 1400,
      distance: '40px',
      easing: 'cubic-bezier(0.5, -0.01, 0, 1.005)',
      origin: 'bottom',
      interval: 200
    })

    sr.reveal('.hero-illustration-browser, .hero-squares', {
      delay: 400,
      duration: 600,
      distance: '40px',
      easing: 'cubic-bezier(0.5, -0.01, 0, 1.005)',
      origin: 'right',
      interval: 150
    })
  }
}())
