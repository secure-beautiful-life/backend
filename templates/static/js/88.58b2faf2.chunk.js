"use strict";(self.webpackChunktestaa=self.webpackChunktestaa||[]).push([[88],{2932:function(n,e,r){r.d(e,{_D:function(){return o},yB:function(){return i}});var t=r(8364).g.injectEndpoints({endpoints:function(n){return{getReview:n.query({query:function(n){var e=n.offset,r=void 0===e?0:e,t=n.limit,i=void 0===t?10:t,o=n.product_id;return{url:"/reviews?product_id=".concat(o,"&offset=").concat(r,"&limit=").concat(i)}},providesTags:["review"]}),postReview:n.mutation({query:function(n){return{url:"/reviews",method:"POST",body:n}},invalidatesTags:["review"]}),deleteReview:n.mutation({query:function(n){var e=n.reviewId;return{url:"/review-service/reviews?reviewId=".concat(e),method:"DELETE"}},invalidatesTags:["review"]})}}}),i=t.useGetReviewQuery,o=t.usePostReviewMutation},4032:function(n,e,r){r.d(e,{Z:function(){return l}});var t,i=r(168),o=r(6444),s=r(6494),a=r(9584),u=r(4373),c=r(6871),d=r(184);function l(n){var e=n.title,r=n.icon,t=n.isBack,i=(0,c.s0)();return(0,d.jsxs)(f,{"data-isback":t,children:[(0,d.jsxs)("div",{children:[t&&(0,d.jsx)(u.u1R,{onClick:function(){return i(-1)},size:"1rem",style:{transform:"translate(-10px,3px)"}}),(0,d.jsx)("span",{children:e})]}),r&&r]})}var f=o.ZP.div(t||(t=(0,i.Z)(["\n  position: fixed;\n  top: 0;\n  width: 100vw;\n  height: 3.4rem;\n  padding: 1.8rem;\n  background-color: #ffffff;\n  z-index: 100;\n  "," "," span {\n    ","\n    ","\n  }\n  svg {\n    width: 1.3rem;\n    height: 1.3rem;\n    ","\n    cursor: pointer;\n  }\n\n  &[data-isback='true'] {\n    & > div {\n      span {\n        position: absolute;\n        right: 50%;\n        transform: translateX(50%);\n      }\n    }\n  }\n"])),(0,s.dG)({js:"space-between"}),(0,s.Bv)(),(0,a.h1)({fontSize:"1.22rem",fontWeight:700}),(0,a.Lq)("BLACK"),(0,a.Lq)("GREY_4"))},1220:function(n,e,r){r.d(e,{Z:function(){return m}});var t,i=r(168),o=r(8062),s=r(5934),a=r(8708),u=r(6444),c=r(9584),d=r(4413),l=r(6494),f=r(184);function m(n){var e=n.type,r=n.icon,t=n.children;return"small"===e?(0,f.jsx)(h,{children:(0,f.jsxs)(f.Fragment,{children:["success"===r&&(0,f.jsx)(o.J5,{autoplay:!0,loop:!0,src:s,style:{height:"80px",width:"80px"}}),"error"===r&&(0,f.jsx)(o.J5,{autoplay:!0,loop:!0,src:a,style:{height:"80px",width:"80px"}}),t]})}):(0,f.jsx)(f.Fragment,{})}var h=u.ZP.div(t||(t=(0,i.Z)(["\n  ","\n  ","\n  ","\n  width: 18rem;\n  height: 14rem;\n  padding: 1rem;\n  border-radius: 2rem;\n  ","\n  gap: 1rem;\n  z-index: 999;\n  + div {\n    width: 100%;\n  }\n  p {\n    ","\n    text-align: center;\n    margin-bottom: 2rem;\n    width: 100%;\n  }\n"])),(0,c.Wf)("WHITE"),(0,l.wm)(),(0,l.dG)({dir:"column",js:"flex-start"}),(0,d.K)("TYPE_A"),(0,c.h1)({fontSize:"1rem"}))},8088:function(n,e,r){r.r(e),r.d(e,{default:function(){return w}});var t=r(8214),i=r(5861),o=r(885),s=r(2791),a=r(8820),u=r(5763),c=r(3452),d=r(6871),l=r(2932),f=r(5017),m=r(9407),h=r(4032),g=r(1220),p=r(4014),v=r(2745),x=r(5472),j=r(184);function w(){var n=(0,s.useState)(0),e=(0,o.Z)(n,2),r=e[0],w=e[1],Z=(0,s.useState)(),b=(0,o.Z)(Z,2),y=b[0],k=b[1],z=(0,p.C)(f.ds),C=(0,s.useState)(""),P=(0,o.Z)(C,2),G=P[0],E=P[1],R=(0,s.useRef)(null),_=(0,c.useDispatch)(),D=(0,d.s0)(),q=(0,p.C)(f.HU),T=(0,l._D)(),W=(0,o.Z)(T,1)[0],F=function(){var n=(0,i.Z)((0,t.Z)().mark((function n(){var e,i;return(0,t.Z)().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:if(!((e=R.current.value).length<1)){n.next=4;break}return E("\ub9ac\ubdf0\ub97c \uc785\ub825\ud574\uc8fc\uc138\uc694"),n.abrupt("return");case 4:i={product_id:q.productId,content:e,images:[{image_string:y,file_name:"name"}],rate:r},console.log(i),W(i).unwrap().then((function(n){window.alert("\ub9ac\ubdf0\uac00 \ub4f1\ub85d\ub418\uc5c8\uc2b5\ub2c8\ub2e4."),D("/")})).catch((function(n){return console.log(n)}));case 7:case"end":return n.stop()}}),n)})));return function(){return n.apply(this,arguments)}}();return(0,s.useEffect)((function(){return function(){_((0,f.$B)())}}),[_]),(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)(h.Z,{title:"\ub9ac\ubdf0 \uc4f0\uae30",isBack:!0}),(0,j.jsxs)(x.Eq,{children:[(0,j.jsxs)(x.bF,{children:[(0,j.jsx)("strong",{children:"\ub9ac\ubdf0\ub97c \uc791\uc131\ud574\uc8fc\uc138\uc694."}),(0,j.jsx)("textarea",{ref:R,placeholder:"\ud14d\uc2a4\ud2b8 \ub9ac\ubdf0"})]}),(0,j.jsxs)(x.bF,{children:[(0,j.jsx)("strong",{children:"\ubcc4\uc810"}),(0,j.jsxs)("div",{children:[r<1?(0,j.jsx)(a.y5j,{size:"2rem",onClick:function(){return w(1)}}):(0,j.jsx)(a.pHD,{size:"2rem",onClick:function(){return w(1)}}),r<2?(0,j.jsx)(a.y5j,{size:"2rem",onClick:function(){return w(2)}}):(0,j.jsx)(a.pHD,{size:"2rem",onClick:function(){return w(2)}}),r<3?(0,j.jsx)(a.y5j,{size:"2rem",onClick:function(){return w(3)}}):(0,j.jsx)(a.pHD,{size:"2rem",onClick:function(){return w(3)}}),r<4?(0,j.jsx)(a.y5j,{size:"2rem",onClick:function(){return w(4)}}):(0,j.jsx)(a.pHD,{size:"2rem",onClick:function(){return w(4)}}),r<5?(0,j.jsx)(a.y5j,{size:"2rem",onClick:function(){return w(5)}}):(0,j.jsx)(a.pHD,{size:"2rem",onClick:function(){return w(5)}})]})]}),(0,j.jsxs)(v.O4,{children:[(0,j.jsx)("strong",{children:"\uc774\ubbf8\uc9c0 \uc120\ud0dd"}),(0,j.jsxs)(v.W5,{children:[(0,j.jsx)("input",{type:"file",id:"imageUrl",onChange:function(n){var e=n.target.files;if(e.length<=0)return console.log("files does not exist");var r=e[0],t=new FileReader;t.readAsDataURL(r),t.onload=function(){var n=t.result;return k(n),n}}}),(0,j.jsx)("label",{htmlFor:"imageUrl",children:(0,j.jsx)(u.ueT,{})})]})]}),(0,j.jsx)(m.Z,{content:"\ub9ac\ubdf0 \ub4f1\ub85d\ud558\uae30",radius:"0.5rem",onClick:F,disabled:0===r})]}),z&&(0,j.jsx)(g.Z,{type:"small",icon:"error",children:(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)("p",{children:G}),(0,j.jsx)(m.Z,{content:"\ud655\uc778",onClick:function(){return _((0,f._K)(!1))},radius:"1.5rem",background:"#9DAABB"})]})})]})}},5472:function(n,e,r){r.d(e,{Eq:function(){return h},NZ:function(){return p},bF:function(){return x},gc:function(){return g},xM:function(){return v},xu:function(){return j}});var t,i,o,s,a,u,c=r(168),d=r(6444),l=r(9584),f=r(6494),m=r(2753),h=d.ZP.div(t||(t=(0,c.Z)(["\n  width: 100%;\n  height: 100vh;\n  overflow-y: scroll;\n  ","\n  ","\n  padding: 5rem 0 3rem 0;\n  strong {\n    font-size: 1.2rem;\n  }\n  + nav {\n    display: none;\n  }\n  button {\n    margin-top: 1rem;\n  }\n  gap: 2rem;\n"])),(0,m.y)(),(0,f.dG)({dir:"column",js:"flex-start",ai:"flex-start"})),g=d.ZP.div(i||(i=(0,c.Z)(["\n  width: 100%;\n  position: relative;\n\n  p {\n    font-size: 1rem;\n    margin-bottom: 0.8rem;\n    line-height: 1.5rem;\n  }\n  strong {\n    font-size: 1rem;\n  }\n\n  & > svg:first-child {\n    position: absolute;\n    right: 0;\n    cursor: pointer;\n  }\n"]))),p=d.ZP.div(o||(o=(0,c.Z)(["\n  ","\n  margin-bottom: 0.8rem;\n  strong {\n    margin-right: 0.5rem;\n  }\n"])),(0,f.dG)({js:"flex-start"})),v=d.ZP.div(s||(s=(0,c.Z)(["\n  ","\n  gap: 1rem;\n  overflow-y: scroll;\n  width: 100%;\n  ","\n  img {\n    width: 5rem;\n    height: 5rem;\n    object-fit: cover;\n  }\n"])),(0,f.dG)({js:"flex-start"}),(0,m.y)()),x=d.ZP.div(a||(a=(0,c.Z)(["\n  width: 100%;\n  ","\n  gap: 1rem;\n  textarea {\n    font-size: 0.9rem;\n    width: 100%;\n    height: 10rem;\n    padding: 0.5rem;\n  }\n  svg {\n    cursor: pointer;\n  }\n  margin-bottom: 1rem;\n"])),(0,f.dG)({dir:"column",js:"flex-start",ai:"flex-start"})),j=d.ZP.div(u||(u=(0,c.Z)(["\n  width: 100%;\n  margin-top: 1.5rem;\n  height: 0.05rem;\n  ","\n"])),(0,l.Wf)("GREY_1"))},2745:function(n,e,r){r.d(e,{Eq:function(){return g},O4:function(){return x},Ph:function(){return w},T7:function(){return v},W5:function(){return j},yh:function(){return p}});var t,i,o,s,a,u,c,d=r(168),l=r(6444),f=r(9584),m=r(6494),h=r(2753),g=l.ZP.div(t||(t=(0,d.Z)(["\n  padding-top: 5rem;\n  padding-bottom: 7.5rem;\n  width: 100%;\n  height: 100vh;\n  overflow-y: scroll;\n  ","\n  button {\n    margin-top: 2rem;\n  }\n"])),(0,h.y)()),p=l.ZP.form(i||(i=(0,d.Z)(["\n  width: 100%;\n  ","\n  gap: 1rem;\n"])),(0,m.dG)({dir:"column",js:"flex-start",ai:"center"})),v=l.ZP.div(o||(o=(0,d.Z)(["\n  ","\n  gap: 1.5rem;\n  margin: 1.5rem 0;\n"])),(0,m.dG)({dir:"column",js:"flex-start",ai:"flex-start"})),x=l.ZP.div(s||(s=(0,d.Z)(["\n  strong {\n    ","\n    display: block;\n    margin-bottom: 0.5rem;\n  }\n"])),(0,f.h1)({fontSize:"1rem",fontWeight:500})),j=l.ZP.div(a||(a=(0,d.Z)(["\n  cursor: pointer;\n  ","\n  width: 5rem;\n  height: 5rem;\n  font-size: 18px;\n  padding: 0 10px;\n  border-radius: 1.1rem;\n  ","\n\n  label {\n    display: inline-block;\n    ","\n    width: 4rem;\n    height: 4rem;\n    ","\n    ","\n    cursor: pointer;\n  }\n  input {\n    position: absolute;\n    width: 0;\n    height: 0;\n    padding: 0;\n    overflow: hidden;\n    border: 0;\n  }\n"])),(0,m.dG)(),(0,f.Wf)("GREY_1"),(0,m.dG)(),(0,f.Lq)("WHITE"),(0,f.h1)({fontSize:"2rem",fontWeight:500})),w=(l.ZP.div(u||(u=(0,d.Z)(["\n  ","\n  gap: 1.5rem;\n  margin: 1.5rem 0;\n"])),(0,m.dG)({dir:"column",js:"flex-start",ai:"flex-start"})),l.ZP.select(c||(c=(0,d.Z)(["\n  width: 50%;\n  height: 2.5rem;\n  border-radius: 1rem;\n  border: none;\n  background-color: #f4f4f4;\n  padding: 0 1rem;\n  margin-bottom: 1rem;\n  &:focus {\n    outline: none;\n  }\n"]))))}}]);
//# sourceMappingURL=88.58b2faf2.chunk.js.map