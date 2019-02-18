
## http
```
brew install httpie
```

## health-check
```
http -v GET localhost:5000/ping
```

## sign-up
```
http -v POST localhost:5000/sign-up name=gavin email=gavin@gavin.com password=test profile=software enginner
```

## tweet
```
http -v POST localhost:5000/tweet id:=1 tweet='First Tweet'
```

## follow
```
http -v POST localhost:5000/follow id:=1 follow:=2
```

## unfollow
```
http -v POST localhost:5000/unfollow id:=1 unfollow:=2
```

## timeline
```
http -v GET localhost:5000/timeline/1
```