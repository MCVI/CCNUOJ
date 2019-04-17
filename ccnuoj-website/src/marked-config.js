import marked from 'marked';
import hljs from 'highlight.js';

marked.setOptions({
  gfm: true,
  tables: true,
  breaks: true,
  pedantic: false,
  sanitize: true,
  smartLists: true,
  smartypants: false,

  highlight: (code) => hljs.highlightAuto(code).value,
});
