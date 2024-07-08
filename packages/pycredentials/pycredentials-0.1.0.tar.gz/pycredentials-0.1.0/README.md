# credentials

**Store your credentials securely.**

## Example

```console
export CREDENTIALS_PATH="./my-important-data"
# create
credentials add my_token deadbeef1234
# modify/create
credentials set my_token dead123409876
# delete
credentials remove my_token
# clear
credentials remove all
# show
credentials show my_token
# show all
credentials show all
```
