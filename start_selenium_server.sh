docker pull selenium/standalone-chrome
docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome:3.141.59-yttrium

set -e
cmd="$@"

n=0
while ! curl -sSL "http://localhost:4444" \
            | jq -r '.value.ready' 2>&1  | grep "true" >/dev/null; do
          n=$(( n + 1 ))
          if [[ "$n" -gt 5 ]]
          then
            break
          else
            echo "waiting for the selenium-standalone server"
          fi
          sleep 1
done

>&2 echo "Selenium driver is now available"
exec  "${cmd}"