"use strict";(self.webpackChunktestaa=self.webpackChunktestaa||[]).push([[185],{2932:function(n,e,t){t.d(e,{_D:function(){return s},yB:function(){return i}});var r=t(569).g.injectEndpoints({endpoints:function(n){return{getReview:n.query({query:function(n){var e=n.offset,t=void 0===e?0:e,r=n.limit,i=void 0===r?10:r,s=n.product_id;return{url:"/reviews?product_id=".concat(s,"&offset=").concat(t,"&limit=").concat(i)}},providesTags:["review"]}),postReview:n.mutation({query:function(n){return{url:"/reviews",method:"POST",body:n}},invalidatesTags:["review"]}),deleteReview:n.mutation({query:function(n){var e=n.reviewId;return{url:"/review-service/reviews?reviewId=".concat(e),method:"DELETE"}},invalidatesTags:["review"]})}}}),i=r.useGetReviewQuery,s=r.usePostReviewMutation},4032:function(n,e,t){t.d(e,{Z:function(){return j}});var r,i=t(168),s=t(6444),o=t(6494),a=t(9584),d=t(4373),u=t(6871),c=t(184);function j(n){var e=n.title,t=n.icon,r=n.isBack,i=(0,u.s0)();return(0,c.jsxs)(l,{"data-isback":r,children:[(0,c.jsxs)("div",{children:[r&&(0,c.jsx)(d.u1R,{onClick:function(){return i(-1)},size:"1rem",style:{transform:"translate(-10px,3px)"}}),(0,c.jsx)("span",{children:e})]}),t&&t]})}var l=s.ZP.div(r||(r=(0,i.Z)(["\n  position: fixed;\n  top: 0;\n  width: 100vw;\n  height: 3.4rem;\n  padding: 1.8rem;\n  background-color: #ffffff;\n  z-index: 100;\n  "," "," span {\n    ","\n    ","\n  }\n  svg {\n    width: 1.3rem;\n    height: 1.3rem;\n    ","\n    cursor: pointer;\n  }\n\n  &[data-isback='true'] {\n    & > div {\n      span {\n        position: absolute;\n        right: 50%;\n        transform: translateX(50%);\n      }\n    }\n  }\n"])),(0,o.dG)({js:"space-between"}),(0,o.Bv)(),(0,a.h1)({fontSize:"1.22rem",fontWeight:700}),(0,a.Lq)("BLACK"),(0,a.Lq)("GREY_4"))},8849:function(n,e,t){t.d(e,{Z:function(){return d}});var r,i=t(168),s=t(8820),o=t(6444),a=t(184);function d(n){var e=n.rate;return(0,a.jsxs)(a.Fragment,{children:[1===e&&(0,a.jsxs)(u,{children:[(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.y5j,{}),(0,a.jsx)(s.y5j,{}),(0,a.jsx)(s.y5j,{}),(0,a.jsx)(s.y5j,{})]}),2===e&&(0,a.jsxs)(u,{children:[(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.y5j,{}),(0,a.jsx)(s.y5j,{}),(0,a.jsx)(s.y5j,{})]}),3===e&&(0,a.jsxs)(u,{children:[(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.y5j,{}),(0,a.jsx)(s.y5j,{})]}),4===e&&(0,a.jsxs)(u,{children:[(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.y5j,{})]}),5===e&&(0,a.jsxs)(u,{children:[(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{}),(0,a.jsx)(s.pHD,{})]})]})}var u=o.ZP.div(r||(r=(0,i.Z)(["\n  svg {\n    width: 1.2rem;\n    height: 1.2rem;\n  }\n"])))},5472:function(n,e,t){t.d(e,{Eq:function(){return f},NZ:function(){return v},bF:function(){return p},gc:function(){return m},xM:function(){return h},xu:function(){return g}});var r,i,s,o,a,d,u=t(168),c=t(6444),j=t(9584),l=t(6494),x=t(2753),f=c.ZP.div(r||(r=(0,u.Z)(["\n  width: 100%;\n  height: 100vh;\n  overflow-y: scroll;\n  ","\n  ","\n  padding: 5rem 0 3rem 0;\n  strong {\n    font-size: 1.2rem;\n  }\n  + nav {\n    display: none;\n  }\n  button {\n    margin-top: 1rem;\n  }\n  gap: 2rem;\n"])),(0,x.y)(),(0,l.dG)({dir:"column",js:"flex-start",ai:"flex-start"})),m=c.ZP.div(i||(i=(0,u.Z)(["\n  width: 100%;\n  position: relative;\n\n  p {\n    font-size: 1rem;\n    margin-bottom: 0.8rem;\n    line-height: 1.5rem;\n  }\n  strong {\n    font-size: 1rem;\n  }\n\n  & > svg:first-child {\n    position: absolute;\n    right: 0;\n    cursor: pointer;\n  }\n"]))),v=c.ZP.div(s||(s=(0,u.Z)(["\n  ","\n  margin-bottom: 0.8rem;\n  strong {\n    margin-right: 0.5rem;\n  }\n"])),(0,l.dG)({js:"flex-start"})),h=c.ZP.div(o||(o=(0,u.Z)(["\n  ","\n  gap: 1rem;\n  overflow-y: scroll;\n  width: 100%;\n  ","\n  img {\n    width: 5rem;\n    height: 5rem;\n    object-fit: cover;\n  }\n"])),(0,l.dG)({js:"flex-start"}),(0,x.y)()),p=c.ZP.div(a||(a=(0,u.Z)(["\n  width: 100%;\n  ","\n  gap: 1rem;\n  textarea {\n    font-size: 0.9rem;\n    width: 100%;\n    height: 10rem;\n    padding: 0.5rem;\n  }\n  svg {\n    cursor: pointer;\n  }\n  margin-bottom: 1rem;\n"])),(0,l.dG)({dir:"column",js:"flex-start",ai:"flex-start"})),g=c.ZP.div(d||(d=(0,u.Z)(["\n  width: 100%;\n  margin-top: 1.5rem;\n  height: 0.05rem;\n  ","\n"])),(0,j.Wf)("GREY_1"))},8185:function(n,e,t){t.r(e),t.d(e,{default:function(){return j}});var r=t(6871),i=t(9664),s=t(2932),o=t(4032),a=t(8849),d=t(2753),u=t(5472),c=t(184);function j(){var n=(0,r.UO)(),e=(0,s.yB)({product_id:Number(n.id),offset:0,limit:10}).data;(0,i.o4)().data;return(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(o.Z,{isBack:!0,title:"\uc0c1\ud488 \ub9ac\ubdf0"}),(0,c.jsxs)(u.Eq,{children:[(0,c.jsxs)("strong",{children:["\ub9ac\ubdf0 ",null===e||void 0===e?void 0:e.totalElements,"\uac1c"]}),null===e||void 0===e?void 0:e.content.map((function(n){return(0,c.jsxs)(u.gc,{children:[(0,c.jsxs)(u.NZ,{children:[(0,c.jsx)("strong",{children:(0,d.q)(n.reviewerName,6)}),(0,c.jsx)(a.Z,{rate:n.rate})]}),(0,c.jsx)("p",{children:n.content}),(0,c.jsx)(u.xM,{children:n.images.length>0&&n.images.map((function(n){return(0,c.jsx)("img",{src:n,alt:"img"})}))}),(0,c.jsx)(u.xu,{})]})}))]})]})}}}]);
//# sourceMappingURL=185.5cc6011b.chunk.js.map