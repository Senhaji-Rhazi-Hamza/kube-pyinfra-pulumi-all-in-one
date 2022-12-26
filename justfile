# behold a recipe
fun:
  echo "hi" > tmp.txt
  cat tmp.txt
  rm tmp.txt

# they can have dependencies
superfun: fun
  echo "woah that was fun!"

# and support other inline scripts
js:
  #!/usr/bin/env node
  console.log('woah, seriously?')

# great for pulling of things that are hard in the shell
ruby:
  #!/usr/bin/env ruby
  puts "yep."