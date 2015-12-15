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
    isConfirm: false,
    confirmMesg: [''],
    confirmCallback: null,
    challenge: {},
    team: {},
    adminCtf: {},
    adminChallenge: {},
    adminTeam: {},
    solvedChallenge: -1,
  },
  store: null,
});
