const MAP = {
  "ko/history": "/about/history/", "ko/bylaws": "/about/bylaws/", "ko/join": "/join/", "ko/submission": "/scripta/submission/", "ko/scripta-about": false,
  "en/history": "/en/about/history/", "en/membership": "/en/membership/", "en/submission": "/en/scripta/submission/", "en/scripta-about": false,
};
const key = d => d.page.inputPath.replace(/^.*\/pages\//, "").replace(/\.md$/, "");
export default {
  eleventyComputed: {
    lang: d => key(d).startsWith("en/") ? "en" : "ko",
    layout: d => (MAP[key(d)] ? "inner.njk" : false),
    permalink: d => (key(d) in MAP ? MAP[key(d)] : false),
  },
};
