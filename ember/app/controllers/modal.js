import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {
    isLogin: false,
    isRegister: false,
    isChallenge: false,
    isTeam: false,
    isProfile: false,
    challenge: {},
    team: {},
    solvedChallenge: false,
  },
  store: null,
  user: {},
  actions: {
    closeModal: function(){
      this.set('modal.isLogin', false);
      this.set('modal.isRegister', false);
      this.set('modal.isChallenge', false);
      this.set('modal.isTeam', false);
      this.set('modal.isProfile', false);
      this.set('store', this.store);
    },
  },
});
