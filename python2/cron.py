#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from crontab import CronTab
import logging, logging.config, yaml, pdb

with open("/vagrant/python/logging-conf.yaml") as f:
    D = yaml.load(f)
    logging.config.dictConfig(D)

my_cron = CronTab(user=True)
my_cron.env['HOME'] = '/vagrant/python'
my_cron.env['SHELL'] = '/bin/bash'
my_cron.env['PATH'] = '/sbin:/bin/:/usr/sbin:/usr/bin'

def create_jobs():
	print 'create a financingChecker task'
	job = my_cron.new(command='/usr/bin/python /vagrant/python/task.py  >> /vagrant/python/crontab.log 2>&1', comment='financingChecker')
	job.minutes.on(0)
	my_cron.write_to_user(user=True)

def remove_job(job):
	my_cron.remove(job)
	pass

def remove_job_byComment(comment):
	my_cron.remove_all(comment=comment)
	pass

def run_job(job):
	job.run()

def find_job(command=None, comment=None, time=None):
	find_commands = {'command': my_cron.find_command,
				'comment': my_cron.find_comment,
				'time': my_cron.find_time}
	if command:
		func = find_commands['command']
		return func(command).next()
	elif comment:
		func = find_commands['comment']
		return func(comment).next()
	elif time:
		func = find_commands['time']
		return func(time).next()
	pass


if __name__ == '__main__':
	print 'cron tab'
	#create_jobs()
	for job in my_cron:
		print job
		#job.run()
	for (name, value) in my_cron.env.items(): #环境变量
		print name
		print value

	aJob = find_job(command='python')
	print aJob
	aJob = find_job(comment='financingChecker')
	print aJob
	aJob = find_job(time='0 * * * *')
	print aJob