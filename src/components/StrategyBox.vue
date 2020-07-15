<template>
  <div>
    <div class="box">
      <h3>
        <span>{{msg.name}}</span>
      </h3>
      <p class="strategy_tips">点击查看</p>
    </div>
  </div>
</template>

<script>
export default {
  props:['msg']
}
</script>

<style scoped>
.strategy_tips {
  position: absolute;
  bottom: 8vh;
  left: 0;
  right: 0;
}
</style>
