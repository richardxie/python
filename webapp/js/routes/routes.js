define([
  'text!templates/Home.html',
  'text!templates/Data.html',
  'text!templates/Signin.html',
  'text!templates/Rules.html'
],function(homeTemplate,dataTemplate, signinTemplate, rulesTemplate){
  return {
    home: {
      title: 'Home'
      , route: '/home'
      , controller: 'home'
      , template: homeTemplate
    }
    , creation: {
      title: 'Data List'
      , route: '/data'
      , controller: 'data'
      , template: dataTemplate
    }
    , signin: {
      title: '签到情况'
      , route: '/signin'
      , controller: 'signin'
      , template: signinTemplate
    }
    , rules: {
      title: '自动投标规则'
      , route: '/rules'
      , controller: 'rules'
      , template: rulesTemplate
    }
  };
})
