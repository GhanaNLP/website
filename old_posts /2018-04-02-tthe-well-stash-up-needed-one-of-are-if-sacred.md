---
layout: post
title: "The well stash up needed one of are if sacred"
post_id: 2
date: 2018-12-05 8:14:30 +0600
tags: education
categories: [Business]
post_image: /assets/img/blog/blog-image-2.jpg
author_name: themeix
comments: true
author_id: 1
---

<p>Jekyll is a simple, blog-aware, static site generator. It takes a template directory containing raw text files in
  various formats, runs it through a converter (like Markdown) and our Liquid renderer, and spits out a complete,
  ready-to-publish static website suitable for serving with your favorite web server.</p>
<p>If you already have a full Ruby development environment with all headers and RubyGems installed, you can create a new
  Jekyll site by doing the following:</p>
<h2 id="how-to-install">How to install<a href="#how-to-install" class="header-link">#</a></h2>
<pre class=" language-javascript">		<code class=" language-javascript">
  # Install Jekyll and Bundler gems through RubyGems
  <span class="token operator">~</span> $ gem install jekyll bundler
  
  # Create a <span class="token keyword">new</span> <span class="token class-name">Jekyll</span> site at <span class="token punctuation">.</span><span class="token operator">/</span>myblog
  <span class="token operator">~</span> $ jekyll <span class="token keyword">new</span> <span class="token class-name">myblog</span>
  
  # Change into your <span class="token keyword">new</span> <span class="token class-name">directory</span>
  <span class="token operator">~</span> $ cd myblog
  
  # Build the site on the preview server
  <span class="token operator">~</span><span class="token operator">/</span>myblog $ bundle exec jekyll serve
  
  # Now browse to http<span class="token punctuation">:</span><span class="token operator">/</span><span class="token operator">/</span>localhost<span class="token punctuation">:</span><span class="token number">4000</span>
</code>	  </pre>
<h2 id="next-steps">Next steps<a href="#next-steps" class="header-link">#</a></h2>
<p>Building a Jekyll site with the default theme is just the first step. The real magic happens when you start creating
  blog posts, using the front matter to control templates and layouts, and taking advantage of all the awesome
  configuration options Jekyll makes available.</p>
<h2 id="basic-usage">Basic usage<a href="#basic-usage" class="header-link">#</a></h2>
<p>The Jekyll gem makes a <code class=" highlighter-rouge language-plaintext">jekyll</code> executable available to you
  in your Terminal window. You can use this command in a number of ways:</p>
<h2 id="directory-structure">Directory structure<a href="#directory-structure" class="header-link">#</a></h2>
<p>Jekyll is, at its core, a text transformation engine. The concept behind the system is this: you give it text written
  in your favorite markup language, be that Markdown, Textile, or just plain HTML, and it churns that through a layout
  or a series of layout files. Throughout that process you can tweak how you want the site URLs to look, what data
  gets displayed in the layout, and more. This is all done through editing text files; the static web site is the
  final product.</p>
<p>A basic Jekyll site usually looks something like this:</p>
<pre class=" language-javascript">		<code class=" language-javascript">
├── _config<span class="token punctuation">.</span>yml
├── _data
<span class="token operator">|</span>   └── members<span class="token punctuation">.</span>yml
├── _drafts
<span class="token operator">|</span>   ├── begin<span class="token operator">-</span><span class="token keyword">with</span><span class="token operator">-</span>the<span class="token operator">-</span>crazy<span class="token operator">-</span>ideas<span class="token punctuation">.</span>md
<span class="token operator">|</span>   └── on<span class="token operator">-</span>simplicity<span class="token operator">-</span><span class="token keyword">in</span><span class="token operator">-</span>technology<span class="token punctuation">.</span>md
├── _includes
<span class="token operator">|</span>   ├── footer<span class="token punctuation">.</span>html
<span class="token operator">|</span>   └── header<span class="token punctuation">.</span>html
├── _layouts
<span class="token operator">|</span>   ├── <span class="token keyword">default</span><span class="token punctuation">.</span>html
<span class="token operator">|</span>   └── post<span class="token punctuation">.</span>html
├── _posts
<span class="token operator">|</span>   ├── <span class="token number">2007</span><span class="token operator">-</span><span class="token number">10</span><span class="token operator">-</span><span class="token number">29</span><span class="token operator">-</span>page<span class="token operator">--</span>nethack<span class="token punctuation">.</span>md
<span class="token operator">|</span>   └── <span class="token number">2009</span><span class="token operator">-</span><span class="token number">04</span><span class="token operator">-</span><span class="token number">26</span><span class="token operator">-</span>barcamp<span class="token operator">-</span>boston<span class="token operator">-</span><span class="token number">4</span><span class="token operator">-</span>roundup<span class="token punctuation">.</span>md
├── _sass
<span class="token operator">|</span>   ├── _base<span class="token punctuation">.</span>scss
<span class="token operator">|</span>   └── _layout<span class="token punctuation">.</span>scss
├── _site
├── <span class="token punctuation">.</span>jekyll<span class="token operator">-</span>metadata
└── index<span class="token punctuation">.</span>html		</code>	  </pre>
<pre class=" language-javascript">		<code class=" language-javascript">
<span class="token keyword">import</span> React<span class="token punctuation">,</span> <span class="token punctuation">{</span> Component <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'react'</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> ReactDOM <span class="token keyword">from</span> <span class="token string">'react-dom'</span><span class="token punctuation">;</span>

<span class="token keyword">class</span> <span class="token class-name">App</span> <span class="token keyword">extends</span> <span class="token class-name">Component</span> <span class="token punctuation">{</span>
<span class="token function">constructor</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
<span class="token keyword">super</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">this</span><span class="token punctuation">.</span>state <span class="token operator">=</span> <span class="token punctuation">{</span>
  hello<span class="token punctuation">:</span> <span class="token string">'Hello World!'</span>
<span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token function">render</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
<span class="token keyword">return</span><span class="token punctuation">(</span>
  <span class="token operator">&lt;</span>div<span class="token operator">&gt;</span>
  <span class="token punctuation">{</span><span class="token keyword">this</span><span class="token punctuation">.</span>state<span class="token punctuation">.</span>hello<span class="token punctuation">}</span>
  <span class="token operator">&lt;</span><span class="token operator">/</span>div<span class="token operator">&gt;</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token punctuation">}</span>

ReactDOM<span class="token punctuation">.</span><span class="token function">render</span> <span class="token punctuation">(</span><span class="token operator">&lt;</span>App <span class="token operator">/</span><span class="token operator">&gt;</span><span class="token punctuation">,</span> document<span class="token punctuation">.</span><span class="token function">getElementById</span><span class="token punctuation">(</span><span class="token string">'root'</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>		  </code>
  </pre>
<h2 id="front-matter">Front matter<a href="#front-matter" class="header-link">#</a></h2>
<p>The front matter is where Jekyll starts to get really cool. Any file that contains a YAML front matter block will be
  processed by Jekyll as a special file. The front matter must be the first thing in the file and must take the form
  of valid YAML set between triple-dashed lines. Here is a basic example:</p>
<p>Between these triple-dashed lines, you can set predefined variables (see below for a reference) or even create custom
  ones of your own. These variables will then be available to you to access using Liquid tags both further down in the
  file and also in any layouts or includes that the page or post in question relies on.</p>
<img src="https://images.unsplash.com/photo-1481487196290-c152efe083f5?ixlib=rb-0.3.5&amp;q=80&amp;fm=jpg&amp;crop=entropy&amp;cs=tinysrgb&amp;w=1920&amp;h=1080&amp;fit=crop&amp;s=80308172730757a7db0434987fa985f3"
  alt="Example image">
<h2 id="where-additional-pages-live">Where additional pages live<a href="#where-additional-pages-live"
      class="header-link">#</a></h2>
<p>Where you put HTML or Markdown files for pages depends on how you want the pages to work. There are two main ways of
  creating pages:</p>
<ul>
  <li>Place named HTML or Markdown files for each page in your site’s root folder.</li>
  <li>Place pages inside folders and subfolders named whatever you want.</li>
</ul>
<p>Both methods work fine (and can be used in conjunction with each other), with the only real difference being the
  resulting URLs. By default, pages retain the same folder structure in <code
      class=" highlighter-rouge language-plaintext">_site</code> as they do in the source directory.</p>
