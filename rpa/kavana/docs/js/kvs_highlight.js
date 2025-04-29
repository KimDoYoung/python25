// Kavana Script 하이라이팅 정의
const kvsKeywords = {
  keyword: [
    "MAIN", "END_MAIN", 
    "ON_EXCEPTION", "END_EXCEPTION", "RAISE",
    "TRY", "CATCH", "FINALLY", "END_TRY",
    "IF", "ELIF", "ELSE", "END_IF",
    "FOR", "TO", "IN", "STEP", "END_FOR",
    "WHILE", "END_WHILE", 
    "FUNCTION", "END_FUNCTION","RETURN",
    "BREAK", "CONTINUE"
  ].join(" "),
  literal: ["True", "False", "None"].join(" ")
};
const basicCommands = [
  "DB CONNECT","DB EXECUTE", "DB QUERY", "DB BEGIN_TRANSACTION", "DB COMMIT", "DB ROLLBACK", "DB CLOSE",
  "INCLUDE", "LOAD_ENV", "SET", "PRINT",
  "JUST", "CONST"
];

const basicCommandRegex = new RegExp(`\\b(${basicCommands.join("|")})\\b`, "i");

hljs.registerLanguage("kvs", function(hljs) {
    return {
      name: "Kavana Script",
      keywords: {
        keyword: kvsKeywords.keyword,
        literal: "True False None"
      },
      contains: [
        hljs.QUOTE_STRING_MODE,    // "Hello"
        hljs.NUMBER_MODE,          // 숫자
        hljs.C_LINE_COMMENT_MODE,   // // 주석
        {
          className: "basic-command",
          begin:basicCommandRegex
        },
      ]
    };
  });
  
  hljs.highlightAll();
  