import markdownIt from "markdown-it";
const mdi = markdownIt({ html: true, breaks: false, linkify: true });
export default function (cfg) {
  cfg.addPassthroughCopy({ "src/assets": "assets" });
  cfg.addPassthroughCopy({ "src/admin": "admin" });
  cfg.addPassthroughCopy({ "src/files": "files" });
  cfg.ignores.add("src/admin/**");
  const byDateDesc = (a, b) => new Date(b.data.date) - new Date(a.data.date);
  cfg.addCollection("notices", c => c.getFilteredByGlob("src/notices/*.md").sort(byDateDesc));
  cfg.addCollection("conferences", c => c.getFilteredByGlob("src/conferences/*.md").sort(byDateDesc));
  cfg.addCollection("volumes", c => c.getFilteredByGlob("src/scripta/vol-*.md").sort((a, b) => b.data.volume - a.data.volume));
  cfg.addFilter("ymd", d => { const x = new Date(d); return `${x.getFullYear()}.${String(x.getMonth()+1).padStart(2,"0")}.${String(x.getDate()).padStart(2,"0")}`; });
  cfg.addFilter("ymKo", d => { const x = new Date(d); return `${x.getFullYear()}년 ${x.getMonth()+1}월`; });
  cfg.addFilter("year", d => new Date(d).getFullYear());
  cfg.addFilter("md", s => mdi.render(s || ""));
  cfg.addFilter("take", (arr, n) => (arr || []).slice(0, n));
  cfg.addFilter("page", (coll, url) => coll.find(p => p.url === url));
  cfg.addFilter("byPath", (coll, frag) => (coll || []).find(p => p.inputPath.includes(frag)));
  return { dir: { input: "src", output: "_site", includes: "_includes", data: "_data" }, markdownTemplateEngine: false, htmlTemplateEngine: "njk" };
}
