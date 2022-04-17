importArticles({
    type: 'script',
    articles: [
        'u:dev:MediaWiki:Tooltips.js',
    ]
});
window.tooltips_list = [
    {
        classname: 'B-Tooltip',
        text: "<#Desc#>",
    },
    {
        classname: 'A-Tooltip',
        parse: '
<div class="container" style="text-align: center;padding-left:20px;">
  <div style="float:right;min-width:1px;position:relative;>
    <#img18#>
      <span style="bottom: 108px;">
        <#number18#>
      </span><br>
     <#img19#>
      <span style="bottom: 54px;">
        <#number19#>
      </span><br>
     <#img20#>
      <span style="bottom: 0px;">
        [[File:Mastery.png| 18px]]
      </span>
  </div>
  <div><#img1#></div>
  <div style="border: none;"></div>
  <div><#img2#></div><br>

  <div><#img3#></div>
  <div><#img4#></div>
  <div><#img5#></div>
  <div><#img6#></div><br>

  <div><#img7#></div>
  <div><#img8#></div>
  <div><#img9#></div>
  <div><#img10#></div>
  <div><#img11#></div><br>

  <div><#img12#></div>
  <div><#img13#></div>
  <div><#img14#></div>
  <div><#img15#></div>
  <div><#img16#></div>
  <div><#img17#></div>
  <div style="border: none;"></div>
</div>',
    },
]
