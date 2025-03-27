// Kavana Script 하이라이팅 정의
hljs.registerLanguage("kvs", function(hljs) {
    return {
      name: "Kavana Script",
      keywords: {
        keyword:
          "MAIN END_MAIN SET PRINT IF ELSE END_IF WHILE END_WHILE FUNCTION END_FUNCTION RETURN TO STEP FOR IN BREAK CONTINUE",
        literal: "True False None"
      },
      contains: [
        hljs.QUOTE_STRING_MODE,    // "Hello"
        hljs.NUMBER_MODE,          // 숫자
        hljs.C_LINE_COMMENT_MODE   // // 주석
      ]
    };
  });
  
  hljs.highlightAll();
  