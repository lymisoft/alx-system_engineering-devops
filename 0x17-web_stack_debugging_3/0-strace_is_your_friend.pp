# 0-strace_is_your_friend.pp
# This Puppet manifest fixes a 500 error caused by a missing PHP module

# Ensure Apache is installed and running
package { 'apache2':
  ensure => installed,
}

# Ensure the necessary PHP module is installed
package { 'php5-mysql':
  ensure => installed,
  require => Package['apache2'],
}

# Ensure Apache is running
service { 'apache2':
  ensure  => running,
  enable  => true,
  require => Package['php5-mysql'],
}
