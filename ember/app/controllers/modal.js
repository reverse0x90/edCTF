import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {
    isLogin: false,
    isRegister: false,
    isChallenge: false,
    isTeam: false,
    isProfile: false,
    isAdminCtf: false,
    isAdminTeam: false,
    isAdminChallenge: false,
    challenge: {},
    team: {},
    adminCtf: {},
    adminChallenge: {},
    adminTeam: {},
    solvedChallenge: -1,
  },
  store: null,
  actions: {
    closeModal: function(){
      this.set('modal.isLogin', false);
      this.set('modal.isRegister', false);
      this.set('modal.isChallenge', false);
      this.set('modal.isTeam', false);
      this.set('modal.isProfile', false);
      this.set('modal.isAdminCtf', false);
      this.set('modal.isAdminTeam', false);
      this.set('modal.isAdminChallenge', false);
      this.set('store', this.store);
    },
  },
});
