// Show the dark variant of the PPoS Dex charts on the dark themes
(() => {
  const DARK_THEMES = ["coal", "navy", "ayu"];
  const CHART = /\/images\/(timeseries|snapshot|insights)\/[a-z_]+\.svg$/;
  const charts = [...document.querySelectorAll("main img")].filter((img) =>
    CHART.test(img.getAttribute("src")),
  );
  const update = () => {
    const html = document.documentElement;
    const dark = DARK_THEMES.some((theme) => html.classList.contains(theme));
    for (const img of charts) {
      const src = img.getAttribute("src").replace(/\.dark\.svg$/, ".svg");
      const wanted = dark ? src.replace(/\.svg$/, ".dark.svg") : src;
      if (img.getAttribute("src") !== wanted) img.setAttribute("src", wanted);
    }
  };
  update();
  new MutationObserver(update).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["class"],
  });
})();
