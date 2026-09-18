(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector('.theme-toggle');
  if (themeButton) {
    const updateThemeLabel = () => themeButton.setAttribute('aria-label', `Switch to ${root.dataset.theme === 'dark' ? 'light' : 'dark'} theme`);
    themeButton.hidden = false;
    updateThemeLabel();
    themeButton.addEventListener('click', () => {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('research-theme', root.dataset.theme); } catch (_) {}
      updateThemeLabel();
    });
  }

  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (menuButton && nav) {
    menuButton.hidden = false;
    nav.classList.add('collapsible');
    const closeMenu = () => {
      nav.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', 'Open navigation');
    };
    menuButton.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', `${open ? 'Close' : 'Open'} navigation`);
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('is-open')) { closeMenu(); menuButton.focus(); } });
    document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
  }

  // Start demos as they enter view; retain explicit pauses across scrolling/filtering.
  const demos = new Map();
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const demoObserver = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    entries.forEach(entry => demos.get(entry.target)?.setVisible(entry.isIntersecting));
  }, { threshold: 0.01 }) : null;
  document.querySelectorAll('.animation-toggle').forEach(button => {
    const image = document.getElementById(button.getAttribute('aria-controls'));
    if (!image?.dataset.animation) return;
    const paper = button.closest('.publication');
    const poster = image.src;
    let playing = false;
    let loading = false;
    let visible = !demoObserver;
    let userPaused = false;
    let manualPlay = false;
    let failed = false;
    let request = 0;
    const pause = () => {
      request++;
      playing = false;
      loading = false;
      image.src = poster;
      button.disabled = false;
      button.removeAttribute('aria-busy');
      button.setAttribute('aria-pressed', 'false');
      button.setAttribute('aria-label', `Play animated demo for ${button.dataset.title}`);
      button.textContent = '▶ Play demo';
    };
    const play = async () => {
      if (playing || loading) return;
      const currentRequest = ++request;
      loading = true;
      button.disabled = true;
      button.setAttribute('aria-busy', 'true');
      button.textContent = 'Loading…';
      try {
        await new Promise((resolve, reject) => {
          const preload = new Image();
          preload.onload = resolve;
          preload.onerror = reject;
          preload.src = image.dataset.animation;
        });
        if (request !== currentRequest) return;
        image.src = image.dataset.animation;
        playing = true;
        const status = document.querySelector('#demo-status');
        if (status) status.textContent = '';
        button.setAttribute('aria-pressed', 'true');
        button.setAttribute('aria-label', `Pause animated demo for ${button.dataset.title}`);
        button.textContent = 'Ⅱ Pause demo';
      } catch (_) {
        if (request !== currentRequest) return;
        failed = true;
        button.textContent = 'Retry demo';
        const status = document.querySelector('#demo-status');
        if (status) status.textContent = 'The animated demo could not load. Please try again.';
      } finally {
        if (request === currentRequest) {
          loading = false;
          button.disabled = false;
          button.removeAttribute('aria-busy');
        }
      }
    };
    const synchronize = () => {
      const shouldPlay = visible && !document.hidden && !paper.hidden && !userPaused && !failed && (!reducedMotion.matches || manualPlay);
      if (shouldPlay) play();
      else if (playing || loading) pause();
    };
    demos.set(paper, {
      synchronize,
      setVisible(value) { visible = value; synchronize(); }
    });
    button.hidden = false;
    button.addEventListener('click', () => {
      if (playing) {
        userPaused = true;
        manualPlay = false;
        pause();
      } else {
        userPaused = false;
        manualPlay = true;
        failed = false;
        play();
      }
    });
    if (demoObserver) demoObserver.observe(paper);
    else synchronize();
  });
  document.addEventListener('visibilitychange', () => {
    demos.forEach(demo => demo.synchronize());
  });
  reducedMotion.addEventListener('change', () => demos.forEach(demo => demo.synchronize()));

  const papers = [...document.querySelectorAll('.publication-list .publication')];
  const controls = document.querySelector('.publication-controls');
  if (controls && papers.length) {
    controls.hidden = false;
    const search = document.querySelector('#publication-search');
    const tabs = [...document.querySelectorAll('.filter-tab')];
    let filter = 'all';
    const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const searchable = papers.map(paper => normalize([
      paper.querySelector('h3')?.textContent,
      paper.querySelector('.publication-authors')?.textContent,
      paper.querySelector('.publication-venue')?.textContent,
      paper.querySelector('.publication-venue')?.title
    ].join(' ')));
    const update = () => {
      const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
      let count = 0;
      papers.forEach((paper, i) => {
        const show = (filter === 'all' || paper.dataset.featured === 'true') && terms.every(term => searchable[i].includes(term));
        paper.hidden = !show;
        demos.get(paper)?.synchronize();
        if (show) count++;
      });
      document.querySelector('#no-publications').hidden = count !== 0;
      document.querySelector('#publication-status').textContent = `${count} ${count === 1 ? 'paper' : 'papers'} shown.`;
    };
    tabs.forEach(tab => tab.addEventListener('click', () => {
      filter = tab.dataset.filter;
      tabs.forEach(item => {
        item.classList.toggle('is-active', item === tab);
        item.setAttribute('aria-pressed', String(item === tab));
      });
      update();
    }));
    search.addEventListener('input', update);
    update();
  }

  document.querySelectorAll('.copy-citation').forEach(button => {
    if (!navigator.clipboard) return;
    button.hidden = false;
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(button.closest('.citation-content').querySelector('code').textContent);
        document.querySelector('#copy-status').textContent = 'Citation copied to clipboard.';
        button.textContent = 'Copied!';
        setTimeout(() => { button.textContent = 'Copy citation'; }, 2200);
      } catch (_) {
        document.querySelector('#copy-status').textContent = 'Please select and copy the citation text.';
        button.textContent = 'Select the text to copy';
      }
    });
  });

  if ('IntersectionObserver' in window) {
    const links = [...document.querySelectorAll('.main-nav a')];
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          links.forEach(link => {
            const active = link.hash === `#${entry.target.id}`;
            link.classList.toggle('is-current', active);
            if (active) link.setAttribute('aria-current', 'location');
            else link.removeAttribute('aria-current');
          });
        }
      });
    }, { rootMargin: '-15% 0px -60% 0px' });
    document.querySelectorAll('main > section[id]').forEach(section => observer.observe(section));
  }
})();
