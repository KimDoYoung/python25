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
          begin:/\b(INCLUDE|ENV_LOAD|SET|PRINT|JUST|CONST)\b/, // bSET, bPRINT, bJUST
        }
      ]
    };
  });
  
  hljs.highlightAll();
  