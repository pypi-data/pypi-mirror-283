

function start_dev() {
  dir="src/pycurses"
  result_files=$(grep -rln "^from pycurses." $dir)
  for file in $result_files; do
    sed -i "" "s|from pycurses.|from |g" $file
  done
  echo "Prepared environment for local development"
}

function publish() {
  dir="src/pycurses"
  imports=$(ls $dir)

  for import in $imports; do
    import_base_name="${import%.*}"
    if [[ $import_base_name == "__init__" ]]; then
      continue
    fi

    results=$(grep -rln "^from ${import_base_name}" $dir)
    for result in $results; do
      search="from ${import_base_name}"
      replace="from pycurses.${import_base_name}"
      sed -i "" "s|$search|$replace|g" $result
    done

  done

  echo "Prepared environment for publishing development"
}

function main() {
  echo "Hello"
  arg="$1"
  if [[ $arg == "dev" ]]; then
    start_dev
  elif [[ $arg == "prepublish" || $arg == "prepub" ]]; then
    publish
  else
    echo "Please pass 'dev' or 'publish'/'pub' to use this script"
  fi
}

main "$@"
