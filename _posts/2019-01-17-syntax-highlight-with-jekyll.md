---
layout: post
title: "Syntax  highlight with jekyll"
post_id: 8
date: 2019-01-17 18:51:30 +0600
tags: [jekyll, update]
categories: [Jekyll, Highlight]
post_image: https://images.pexels.com/photos/1366901/pexels-photo-1366901.jpeg?auto=compress&cs=tinysrgb&h=650&w=940
author_name: Themeix
comments: true
author_id: 3
---

<h1>Markup</h1>
<p>To use this language, use one of the following classes:</p>
<ul>
  <li><code class=" language-none">"language-markup"</code></li>
  <li><code class=" language-none">"language-html"</code></li>
  <li><code class=" language-none">"language-xml"</code></li>
  <li><code class=" language-none">"language-svg"</code></li>
  <li><code class=" language-none">"language-mathml"</code></li>
  <li><code class=" language-none">"language-ssml"</code></li>
  <li><code class=" language-none">"language-atom"</code></li>
  <li><code class=" language-none">"language-rss"</code></li>
</ul>
<h2>Empty tag</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span></code></pre>
<h2>Tag that spans multiple lines</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span>
<span class="token punctuation">&gt;</span></span>hello!
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span></code></pre>
<h2>Name-attribute pair</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span></code></pre>
<h2>Name-attribute pair without quotes</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span>prism</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span></code></pre>

<h2>Attribute without value</h2>
<pre class=" language-markup"><code class=" language-markup"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span> <span class="token attr-name">data-foo</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span> <span class="token attr-name">data-foo</span> <span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>p</span><span class="token punctuation">&gt;</span></span>
</code></pre>

<h2>Namespaces</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span><span class="token namespace">html:</span>p</span> <span class="token attr-name"><span class="token namespace">foo:</span>bar</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>baz<span class="token punctuation">"</span></span> <span class="token attr-name"><span class="token namespace">foo:</span>weee</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span><span class="token namespace">html:</span>p</span><span class="token punctuation">&gt;</span></span></code></pre>

<h2>XML prolog</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token prolog">&lt;?xml version="1.0" encoding="utf-8"?&gt;</span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>svg</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>svg</span><span class="token punctuation">&gt;</span></span></code></pre>
<h2>DOCTYPE</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token doctype"><span class="token punctuation">&lt;!</span><span class="token doctype-tag">DOCTYPE</span> <span class="token name">html</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>html</span><span class="token punctuation">&gt;</span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>html</span><span class="token punctuation">&gt;</span></span></code></pre>

<h2>CDATA section</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span><span class="token namespace">ns1:</span>description</span><span class="token punctuation">&gt;</span></span><span class="token cdata">&lt;![CDATA[
  CDATA is &lt;not&gt; magical.
]]&gt;</span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span><span class="token namespace">ns1:</span>description</span><span class="token punctuation">&gt;</span></span></code></pre>
<h2>Comment</h2>
<pre class=" language-markup"><code class=" language-markup"><span class="token comment">&lt;!-- I'm a comment --&gt;</span>
And i'm not</code></pre>

<h2>Entities</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token entity named-entity" title="&amp;">&amp;amp;</span> <span class="token entity" title="♥">&amp;#x2665;</span> <span class="token entity" title="&nbsp;">&amp;#160;</span> <span class="token entity" title="Œ">&amp;#x152;</span></code></pre>
<h2>Embedded JS and CSS</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token doctype"><span class="token punctuation">&lt;!</span><span class="token doctype-tag">DOCTYPE</span> <span class="token name">html</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>html</span> <span class="token attr-name">lang</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>en<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>head</span><span class="token punctuation">&gt;</span></span>
  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>meta</span> <span class="token attr-name">charset</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>utf-8<span class="token punctuation">"</span></span> <span class="token punctuation">/&gt;</span></span>
  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>title</span><span class="token punctuation">&gt;</span></span>I can haz embedded CSS and JS<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>title</span><span class="token punctuation">&gt;</span></span>
  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>style</span><span class="token punctuation">&gt;</span></span><span class="token style"><span class="token language-css">
    <span class="token atrule"><span class="token rule">@media</span> print</span> <span class="token punctuation">{</span>
      <span class="token selector">p</span> <span class="token punctuation">{</span> <span class="token property">color</span><span class="token punctuation">:</span> red <span class="token important">!important</span><span class="token punctuation">;</span> <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
  </span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>style</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>head</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>body</span><span class="token punctuation">&gt;</span></span>
  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>h1</span><span class="token punctuation">&gt;</span></span>I can haz embedded CSS and JS<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>h1</span><span class="token punctuation">&gt;</span></span>
  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>script</span><span class="token punctuation">&gt;</span></span><span class="token script"><span class="token language-javascript">
  <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token boolean">true</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    console<span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'foo'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
  </span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>script</span><span class="token punctuation">&gt;</span></span>

<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>body</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>html</span><span class="token punctuation">&gt;</span></span></code></pre>
<h2>Invalid HTML</h2>
<pre
  class=" language-markup"><code class=" language-markup">&lt;l <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>ul</span><span class="token punctuation">&gt;</span></span></code></pre>
<h2>Multi-line attribute values</h2>
<pre class=" language-markup"><code class=" language-markup"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>p</span> <span class="token attr-name">title</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>foo
bar
baz<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span></code></pre>
<h2>XML tags with non-ASCII characters</h2>
<pre
  class=" language-markup"><code class=" language-markup"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>Läufer</span><span class="token punctuation">&gt;</span></span>foo<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>Läufer</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>tag</span> <span class="token attr-name">läufer</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>läufer<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>bar<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>tag</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span><span class="token namespace">läufer:</span>tag</span><span class="token punctuation">&gt;</span></span>baz<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span><span class="token namespace">läufer:</span>tag</span><span class="token punctuation">&gt;</span></span></code></pre>