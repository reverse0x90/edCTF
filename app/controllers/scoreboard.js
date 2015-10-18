import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  ctf: undefined,
  options: undefined,
  c3Options: {
    axis: {
      x: {
        tick: {
          fit: true,
          format: '%Y-%m-%d',
          outer: false,
        },
        type: 'timeseries',
      },
      y: {
        //show: false,
        min: 0,
        color: 'white',
        padding: {
          top:0,
          bottom:0
        },
        tick: {
          fit: true,
          outer: false,
        },
      },
    },
    point: {
      show: false
    },
    grid: {
      y: {
        show: true
      },
    },
  },
  setOptions: function(){
    var options = {
      width: 1000,
      height: this.get('ctf.scoreboard.numtopteams')*34,
      vAxis: {
        format: 'decimal',
      },
      hAxis: {
        maxTextLines: 100,
      },
      //selectionMode: 'multiple',
    };
    this.set('options', options);
  }.observes('ctf.scoreboard.numtopteams').on('init'),
  actions:{
    openTeamView: function(id){
      this.store.find('team', id).then((team) => {
        this.set('modal.team', team);
      });
      this.set('modal.isTeam', true);
    }
  },
});
