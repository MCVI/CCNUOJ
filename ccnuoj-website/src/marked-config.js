import marked from 'marked';
import hljs from 'highlight.js';
import 'highlight.js/styles/googlecode.css';

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
