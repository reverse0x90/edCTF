import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {
    isLogin: false,
    isRegister: false,
    isChallenge: false,
    isTeam: false,
    challenge: {},
    team: {},
  },
  actions: {
    closeModal: function(){
      this.set('modal.isLogin', false);
      this.set('modal.isRegister', false);
      this.set('modal.isChallenge', false);
      this.set('modal.isTeam', false);
    },
  },
});
