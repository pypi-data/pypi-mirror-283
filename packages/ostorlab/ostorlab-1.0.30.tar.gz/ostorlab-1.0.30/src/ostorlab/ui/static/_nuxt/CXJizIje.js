var $=Object.defineProperty;var h=(o,a,e)=>a in o?$(o,a,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[a]=e;var l=(o,a,e)=>(h(o,typeof a!="symbol"?a+"":a,e),e);function u(o,...a){let e="",t;for(t=0;t<a.length;t++)e+=o[t]+a[t];return e+=o[t],e}const T="X-Api-Key";class A{constructor(a){l(this,"$axios");this.$axios=a}_createAuthorizationHeader(a){return{[T]:a.apiKey}}async post(a,e){if(a!=null)return await this.$axios.post(a.endpoint,e,{headers:this._createAuthorizationHeader(a)})}}const f=u`query scans($scanIds: [Int], $page: Int, $numberElements: Int, $orderBy: OxoScanOrderByEnum, $sort: SortEnum) {
  scans(scanIds: $scanIds, page: $page, numberElements: $numberElements, orderBy: $orderBy, sort: $sort) {
    pageInfo {
      count
      numPages
    }
    scans {
      id
      title
      assets {
        __typename
        ... on OxoAndroidFileAssetType {
          id
          type
          scanId
          packageName
          path
        }
        ... on OxoIOSFileAssetType {
          id
          type
          bundleId
          path
        }
        ... on OxoAndroidStoreAssetType {
          id
          type
          applicationName
        }
        ... on OxoIOSStoreAssetType {
          id
          type
          bundleId
          applicationName
        }
        ... on OxoUrlAssetType {
          id
          type
          links
        }
        ... on OxoNetworkAssetType {
          id
          type
          networks
        }
      }
      createdTime
      progress
    }
  }
}
`,g=u`
query Scan($scanId: Int!) {
  scan(scanId: $scanId) {
      id
      title
      createdTime
      messageStatus
      progress
  }
}
`,O=u`mutation deleteScan($scanId: Int!) {
  deleteScan(scanId: $scanId) {
    result
  }
}
`,E=u`mutation stopScan($scanId: Int!) {
  stopScan(scanId: $scanId) {
    scan {
      id
    }
  }
}`,N=u`mutation ImportScan($file: Upload!, $scanId: Int) {
  importScan(file: $file, scanId: $scanId) {
    message
  }
}`,_=u`
  mutation RunScan ($scan: OxoAgentScanInputType!) {
    runScan (scan: $scan) {
      scan {
        id
      }
    }
  }
`;class b{constructor(a){l(this,"requestor");l(this,"totalScans");this.requestor=new A(a),this.totalScans=0}async getScans(a,e){var s,d,r,c,i;e={...e},e.numberElements===-1&&(e.numberElements=void 0,e.page=void 0);const t=await this.requestor.post(a,{query:f,variables:e}),n=((s=t==null?void 0:t.data)==null?void 0:s.data.scans.scans)||[];return this.totalScans=((i=(c=(r=(d=t==null?void 0:t.data)==null?void 0:d.data)==null?void 0:r.scans)==null?void 0:c.pageInfo)==null?void 0:i.count)||n.length,n}async getScan(a,e){var n,s;const t=await this.requestor.post(a,{query:g,variables:{scanId:e}});return((s=(n=t==null?void 0:t.data)==null?void 0:n.data)==null?void 0:s.scan)||{}}async stopScan(a,e){var n,s;const t=await this.requestor.post(a,{query:E,variables:{scanId:e}});return((s=(n=t==null?void 0:t.data)==null?void 0:n.stopScan)==null?void 0:s.result)||!1}async deleteScan(a,e){var n,s;const t=await this.requestor.post(a,{query:O,variables:{scanId:e}});return((s=(n=t==null?void 0:t.data)==null?void 0:n.deleteScan)==null?void 0:s.result)||!1}async importScan(a,e,t){var c,i;const n=new FormData,s=N,d={scanId:t,file:null};n.append("operations",JSON.stringify({query:s,variables:d,app:e,maps:{app:["variables.file"]}})),n.append("0",e),n.append("map",JSON.stringify({0:["variables.file"]}));const r=await this.requestor.$axios.post(a.endpoint,n,{headers:{"Content-Type":"multipart/form-data","X-Api-Key":a.apiKey}});return((i=(c=r==null?void 0:r.data)==null?void 0:c.importScan)==null?void 0:i.result)||!1}async runScan(a,e){var n,s,d,r,c,i,p,S,I,m,y;const t=await this.requestor.post(a,{query:_,variables:{scan:e}});if((((n=t==null?void 0:t.data)==null?void 0:n.errors)||[]).length>0)throw new Error((d=(s=t==null?void 0:t.data)==null?void 0:s.errors[0])==null?void 0:d.message);if(((c=(r=t==null?void 0:t.data)==null?void 0:r.data)==null?void 0:c.runScan)===null||((p=(i=t==null?void 0:t.data)==null?void 0:i.data)==null?void 0:p.runScan)===void 0)throw new Error("An error occurred while creating the scan");return(y=(m=(I=(S=t==null?void 0:t.data)==null?void 0:S.data)==null?void 0:I.runScan)==null?void 0:m.scan)==null?void 0:y.id}}export{A as R,b as S,u as g};
