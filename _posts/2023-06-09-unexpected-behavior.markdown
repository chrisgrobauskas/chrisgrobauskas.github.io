---
layout: post
title:  "Unexpected Behavior"
date:   2023-06-09 08:00:00 -0500
categories: coding
---
> “Seek simplicity and distrust it.” ~ [Alfred Whitehead](https://en.wikipedia.org/wiki/Alfred_North_Whitehead)

As an example of something simple that you might want to distrust, let us look at default error handling in ```bash```.  

You can cut & paste the short scripts below into bash to follow along.

### Failure Is An Option
Script:
{% highlight bash %}
false
echo $?
{% endhighlight %}

Result:
```
1
```
This is simple enough.  The ```false``` command sets a return code of 1.  The ```echo $?``` displays the return code for the last command.

### Script Return Codes
If I put the same code in a bash script, you get the same result.

Script:
{% highlight bash %}
cat > notok.sh << SCRIPTEND
#!/bin/bash
false
SCRIPTEND
chmod +x notok.sh
./notok.sh
echo $?
{% endhighlight %}
Result:
```
1
```

### Here Documents
The example above uses a "Here Document" (```<< SCRIPTEND``` to ```SCRIPTEND```).  "Here Documents" are a topic for another blog, but they allow you to label a section of inline text to be passed to other parts of a script. 

In this case, the script between the labels is passed to the ```cat > notok.sh``` file redirection statement to create a script.

To see what is written to the notok.sh script, just ```cat``` the file created.

Command:
```
cat notok.sh
```

Output:
```
#!/bin/bash
false
```

### Multiple Return Codes
Now that we have a basic script to start with … what happens if I add another command that does not set a return code of 1?  

In this case, there is a return code of 1 (```false```) followed by a return code of 0 (```true```) in the script.

Script:
{% highlight bash %}
cat > notok.sh << SCRIPTEND
#!/bin/bash
false
true
SCRIPTEND
chmod +x notok.sh
./notok.sh
echo $?
{% endhighlight %}
Result:
```
0
```

### Last Return Code Wins
We can learn two things: 1) the script is returning the return code from the ```true``` command 2) the script is *not* exiting on non-zero return codes.

While we could argue whether this is a sensible behavior, it is the expected behavior for bash. 

Personally, I prefer scripts to exit on unexpected return codes.  

### It's a Trap!
One way to make a script exit on a non-zero return code is to add an error trap.

> Note the ```\``` characters below are only there to keep the variables in the here document from being expanded before being written to the script file.


Script:
{% highlight bash %}
cat > notok.sh << SCRIPTEND
#!/bin/bash

trap 'on_err \$? \$LINENO' ERR

on_err() {
  echo "Error: Unexpected return code \$1 on line \$2"
  exit 1;
}

false
true
SCRIPTEND
chmod +x notok.sh
./notok.sh
echo $?
{% endhighlight %}
Result:
```
Error: Unexpected return code 1 on line 10
1
```

The ```trap 'on_err $? $LINENO' ERR``` statement does the following: 

- Catches errors with ```ERR``` keyword
- Calls the ```on_err()``` function passing the return code ```$?``` and ```$LINENO```
- The function ```on_err()``` then shows the return code and line number information before exiting with a return code of 1

You can see from the ```cat -n``` command below it is finding the correct line number via the ```$LINENO``` variable.  This shell variable is managed by bash.

Command:
```
cat -n notok.sh
```

Output:
```
cat -n notok.sh
 1	#!/bin/bash
 2	
 3	trap 'on_err $? $LINENO' ERR
 4	
 5	on_err() {
 6	  echo "Error: Unexpected return code $1 on line $2"
 7	  exit 1;
 8	}
 9	
10	false
11	true

```

> The function name does not have to be on_err, and it could also perform cleanup before exiting.  One example could be cleaning up files created by ```mktemp``` if that was used earlier in the script.

But what happens if I put the false statement followed by a true statement inside a function?  Depending on your background, you might expect it to still trap the error, but you would be wrong.

{% highlight bash %}
cat > notok.sh << SCRIPTEND
#!/bin/bash

trap 'on_err \$? \$LINENO' ERR

on_err() {
  echo "Error: Unexpected return code \$1 on line \$2"
  exit 1;
}

run_it() {
  false
  true
}
run_it
SCRIPTEND
chmod +x notok.sh
./notok.sh
echo $?
{% endhighlight %}
Result:
```
0
```

Why the difference in behavior?  By default, in bash a function returns the last return code, and that is the return code which would be trapped (if any).

You can turn on an option, however, to tell the script to trap return codes in functions: ```set -E``` 

{% highlight bash %}
cat > notok.sh << SCRIPTEND
#!/bin/bash
set -E

trap 'on_err \$? \$LINENO' ERR

on_err() {
  echo "Error: Unexpected return code \$1 on line \$2"
  exit 1;
}

run_it() {
  false
  true
}
run_it
SCRIPTEND
chmod +x notok.sh
./notok.sh
echo $?
{% endhighlight %}
Result:
```
Error: Unexpected return code 1 on line 11
1
```

Are we there yet?  Well it depends on if you care about unexpected return codes within pipelines.  

Consider the following:

{% highlight bash %}
cat > notok.sh << SCRIPTEND
#!/bin/bash
set -E

trap 'on_err \$? \$LINENO' ERR

on_err() {
  echo "Error: Unexpected return code \$1 on line \$2"
  exit 1;
}

run_it() {
  false | tee
  true
}
run_it
SCRIPTEND
chmod +x notok.sh
./notok.sh
echo $?
{% endhighlight %}
Result:
```
0
```
Adding ```| tee``` above means the pipeline returns a return code of 0 instead of the 1 that is set by false.  If we want to trap these errors too, we can add ```set -o pipefail```.

Whether you want to trap pipeline errors depends on what you want your scripts to do.

> If you turn on ```pipefail``` you might be surprised by grep when it does not match a search string.  In that case, grep sets ```$?``` equal to 1.


{% highlight bash %}
cat > notok.sh << SCRIPTEND
#!/bin/bash
set -E
set -o pipefail

trap 'on_err \$? \$LINENO' ERR

on_err() {
  echo "Error: Unexpected return code \$1 on line \$2"
  exit 1;
}

run_it() {
  true | grep "epic fail"
}
run_it
SCRIPTEND
chmod +x notok.sh
./notok.sh
echo $?
{% endhighlight %}
Result:
```
Error: Unexpected return code 1 on line 12
1
```

## In Summary
```
#!/bin/bash
set -E
set -o pipefail

trap 'on_err $? $LINENO' ERR

on_err() {
  echo "Error: Unexpected return code $1 on line $2"
  exit 1;
}
```

You can set a trap to catch errors in your scripts that use functions and pipelines by adding the above code.

Happy coding!