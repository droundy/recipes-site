#!/usr/bin/python2

import responsive

nav = responsive.FixedOrWide('nav', 12, widecss="""
    height: 2em;
    min-width: 23em;
    ul li{display:block;position:relative;float:left;margin:0;height:2em;}
    ul li a{height:2em;padding-right:0.5em;padding-left:0.5em;
       border-right:.1em solid #000;
       border-left:.2em solid $menuback;
    }
    ul li a.current:before,
    ul li a.current:hover:before{
        left: #{-$leftboxsize/2+0.1em};
    }
    img {
       height: 2em;
       display: none;
       float: left;
    }
    @media screen and (min-width: 27em) {
        img { display: block; }
    }
""", fixedcss = """
    height: auto;
    min-width: 0;
    ul li{display:block;float:none;margin:0;height:auto;}
    ul li a{height:auto;padding-left:1em;padding-right:0;}
    .menu-heading {
        width: 100%;
    }
    ul li a.current:before,
    ul li a.current:hover:before{
        left: 0;
    }
    img {
       height: auto;
       display: block;
       float: none;
    }
""")
#header = responsive.Optional('header', 30)
article = responsive.Column('article', 29)
toc = responsive.Fixed('aside.toc', 15)
header = responsive.Column('header', 41)
#main = responsive.Container('main', [header, article])
main = responsive.Column('main', 29)
html = responsive.EmContainer('', [nav], main, [toc])

print responsive.total_css(html, """
$black: #000;
$white: #fff;

$highlight: #1f8dd6;
$backhighlight: #cbe7f8;

$hoverfocus: #f00;

$menuback: #191818;
$menuhoverback: #444;
$menufore: #999;
$menuitem: #333;
$menushadow: #000;
$menuwidth: 150px;
$leftboxsize: 1.0em; /* actually circle in menu */

$contentcolor: #555;

$maintoc: #999;
$secondtoc: #666;

html { /* make scrollbar always visible */
overflow: -moz-scrollbars-vertical;
overflow-y: scroll;
}

body { /* just define the font once! */
    font:normal 1em Helvetica, Verdana, Arial, sans-serif;
}

@mixin border-radius($radius) {
    -webkit-border-radius: $radius;
    -moz-border-radius: $radius;
    -ms-border-radius: $radius;
    border-radius: $radius;
}

/*
Add transition to containers so they can push in and out.
*/
nav,
main,
.menu-link {
    -webkit-transition: all 0.2s ease-out;
    -moz-transition: all 0.2s ease-out;
    -ms-transition: all 0.2s ease-out;
    -o-transition: all 0.2s ease-out;
    transition: all 0.2s ease-out;
}

article {
    /*max-width: 40em;*/
    margin-bottom: 3em;
    line-height: 1.6em;
    color: $contentcolor;
    a {
        color: $highlight;
        text-decoration: none;
    }
    a:visited {
        color: $black;
    }
    a:hover,
    a:focus {
        color: $hoverfocus;
    }
    a:active {
        padding-top: 0.125em;
    }

    /* css list with circle background -------------- */
    ol,
    ul{
        counter-reset: li;
        list-style: none;
        padding: 0;
        margin-bottom: 4em;
    }
    ol ol{
        margin: 0 0 0 2em;
    }
    ol li,
    ul li{
        position: relative;
        display: block;
        padding: .0em .0em .0em 1.1em;
        margin-left: 1em;
        background: $white;
        text-decoration: none;
        @include border-radius(.3em);
    }
    ol li:hover,
    ul li:hover{
        background: $backhighlight;
    }
    ol li:before,
    ul li:before{
        $circlediameter: 2.0em;
        position: absolute;
        left: #{-$circlediameter/2};
        top: 50%;
        margin-top: #{-$circlediameter + 1.0em};
        background: $highlight;
        height: $circlediameter;
        width: $circlediameter;
        line-height: #{$circlediameter - 0.5em};
        border: .3em solid $white;
        text-align: center;
        font-weight: bold;
        font-size: 1em;
        @include border-radius($circlediameter);
        color:$white;
    }
    ul li:before{
        content: ">";
    }
    ol li:before{
        content: counter(li);
        counter-increment: li;
    }
}


aside.toc {
    background: $menuback;

    padding-top: 2em;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    color: $white;
    ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    a {
        display: block;
        text-decoration: none;
        color: $maintoc;
        border: none;
        padding-left: 0.8em;
        padding-right: 0.8em;
        padding-bottom: 0.3em;
        padding-top: 0.3em;
    }
    ul li ul li a {
        color: $secondtoc;
        border: none;
        font-size: 0.9em;
        padding-left: 1.5em;
    }
    ul {
        border: none;
        background: transparent;
        li a:hover,
        aside.toc ul li a:focus {
            color: $highlight;
        }
    }
}

header {
    background-color: $white;
    text-align: center;
    h1 {
        margin: 0.2em 0;
        font-size: 2em;
        font-weight: 300;
        color: $highlight;
    }
    h2 {
        font-weight: 300;
        color: $black;
        padding: 0;
        margin-top: 0;
    }
 }

/*
The `#menu` `<div>` is the parent `<div>` that contains the `.pure-menu` that
appears on the left side of the page.
*/

nav {
    .menu-heading {
        background: $highlight;
    }
    background: $menuback;

    ul {
        margin:0;
        padding:0;list-style-type:none;display:block;
        font-weight:bold;
        line-height:165%;
        width:100%;
    }

    ul li{margin:0;padding:0;border-top:.15em solid $menuback;
          border-bottom:.15em solid $menushadow;}

    ul li a{display:block;text-decoration:none;color:$menufore;
background:$menuitem;padding:0 0 0 1.25em;width:100%;}

    ul li a:hover{
background:$menuhoverback;}

    ul li a.current,
    ul li a.current:hover{
       background:$menuhoverback;
    }
    ul li a.current:before,
    ul li a.current:hover:before{
        content: "";
        position: absolute;
        margin-top: #{-0*$leftboxsize + 0.3em};
        background: $highlight;
        height: $leftboxsize;
        width: $leftboxsize;
        line-height: #{$leftboxsize};
        text-align: center;
        font-weight: bold;
        font-size: 1em;
        @include border-radius($leftboxsize);
        color:$white;
    }
}

/* -- Dynamic Button For Responsive Menu -------------------------------------*/

/*
The button to open/close the Menu is custom-made and not part of Pure. Here's
how it works:
*/

/*
`.menu-link` represents the responsive menu toggle that shows/hides on
small screens.
*/
.menu-link {
    position: fixed;
    display: block; /* show this only on small screens */
    top: 0;
    left: 0; /* "#menu width" */
    /* background: rgba(31,141,214,.3); */
    background: rgba(0,0,0,0);
    font-size: .7em; /* change this value to increase/decrease button size */
    z-index: 10;
    width: 3em;
    height: auto;
    padding: 1.7em .7em;
}

    .menu-link:hover,
    .menu-link:focus {
        background: rgba(31,141,214,.6);
    }

    .menu-link span {
        position: relative;
        display: block;
    }

    .menu-link span,
    .menu-link span:before,
    .menu-link span:after {
        background-color: $black;
        width: 100%;
        height: 0.375em;
        @include border-radius(25em);
    }

        .menu-link span:before,
        .menu-link span:after {
            position: absolute;
            margin-top: -1.0em;
            content: " ";
        }

        .menu-link span:after {
            margin-top: 1.0em;
        }

""")
