board = [0,3,4,1,7,0,5,0,0,
         0,6,0,0,0,8,3,0,1,
         7,0,0,3,0,0,0,0,6,
         5,0,0,6,4,0,8,0,7,
         0,1,0,9,0,0,0,6,0,
         3,0,6,0,0,2,0,0,4,
         8,0,0,0,0,9,0,0,2,
         1,0,3,7,0,0,0,9,0,
         0,0,9,0,3,1,7,4,0]

newboard xs ys = foldl (\acc x -> merge (break (==0) acc) x) xs ys where merge (f,0:t) x = f ++ [x] ++ t

pointget bd = [1..9] \\ [bd!!(x*9+y) | x<-[0..8], y<-[0..8], x==row||y==col||(f' x, f' y)==(f' row, f' col)] where
                                (row, col) = divMod (length (takeWhile (/=0) bd)) 9
                                f' x = x `div` 3 * 3

nextanswer answer = map (\x->answer++[x]) (pointget $ newboard board answer)

sudoku = (iterate (concatMap $ nextanswer) [[]]) !! length (filter (== 0) board)

divide bd = unfoldr (\x -> if x == [] then Nothing else Just (splitAt 9 x)) bd

main = mapM_ (\x -> putStrLn "answer:" >> mapM_ print (divide $ newboard board x) >> putStrLn "") sudoku