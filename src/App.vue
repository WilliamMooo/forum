<template>
  <div id="app" class="app">
  <transition name="fade" mode="out-in">
    <router-view/>
  </transition>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
}
a {
  text-decoration: inherit;
}
ul,
ol {
  list-style: none;
}
input,
select,
button {
  font: inherit;
}
html,
body {
  height: 100%;
}
body {
  background-color: #1abc9c; 
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}
.app {
  display: flex;
  height: 100%;
  align-items: center;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
::-webkit-scrollbar {
  /*隐藏滚轮*/
  display: none;
}
</style>

<script>
// export default {
//   mounted() {
//     let sha256 = require("js-sha256").sha256
//     console.log(sha256('961017025'))
//   }
// }
</script>