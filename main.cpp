#include <bits/stdc++.h>
using namespace std;

enum class Color { White, Black };
enum class PieceType { King, Queen, Rook, Knight, Bishop, Pawn };

class Chessboard;  

class ChessPiece {
public:
    PieceType type;
    Color color;
    ChessPiece(PieceType _type, Color _color) : type(_type), color(_color) {}

    bool isDiagonalMove(int fromX, int fromY, int toX, int toY) const {
        int dx = abs(toX - fromX);
        int dy = abs(toY - fromY);
        return dx == dy;
    }

    bool isVerticalOrHorizontalMove(int fromX, int fromY, int toX, int toY) const {
        return (fromX == toX) || (fromY == toY);
    }

    friend bool isValidMove(const ChessPiece& piece, int fromX, int fromY, int toX, int toY, const Chessboard& board);
};

class Chessboard {
private:
    map<pair<int, int>, shared_ptr<ChessPiece>> board;

public:
    shared_ptr<ChessPiece> getPiece(int x, int y) const {
         
    }

    bool isOccupied(int x, int y) const {
        
    }

    bool isValidPosition(int x, int y) const {
         
    }

    Color getCurrentPlayerColor() const {
        
    }

    
};

bool isValidVerticalOrHorizontalMove(int fromX, int fromY, int toX, int toY, const Chessboard& board) {
    if (fromX != toX && fromY != toY) {
        return false;  
    }

    int dx = (toX > fromX) ? 1 : ((toX < fromX) ? -1 : 0);
    int dy = (toY > fromY) ? 1 : ((toY < fromY) ? -1 : 0);
    int x = fromX + dx;
    int y = fromY + dy;

    while (x != toX || y != toY) {
        if (board.isOccupied(x, y)) {
            return false; 
        }

        x += dx;
        y += dy;
    }

    shared_ptr<ChessPiece> destinationPiece = board.getPiece(toX, toY);
    if (destinationPiece && destinationPiece->color == board.getPiece(fromX, fromY)->color) {
        return false;  
    }

    return true;
}
 

bool isValidMove(int fromX, int fromY, int toX, int toY, Color playerColor, const Chessboard& board) {
    int dx = abs(toX - fromX);
    int dy = abs(toY - fromY);
    
    if (dx != dy) {
        return false;  
    }
    
    int xDirection = (toX > fromX) ? 1 : -1;
    int yDirection = (toY > fromY) ? 1 : -1;
    
    int x = fromX + xDirection;
    int y = fromY + yDirection;
    
    while (x != toX && y != toY) {
        if (board.isOccupied(x, y)) {
            return false;  
        }
        x += xDirection;
        y += yDirection;
    }
    
    shared_ptr<ChessPiece> destinationPiece = board.getPiece(toX, toY);
    if (destinationPiece && destinationPiece->color == playerColor) {
        return false;  
    }
    
    return true;  
}


 
class Bishop : public ChessPiece {
public:
    Bishop(Color _color) : ChessPiece(PieceType::Bishop, _color) {}

    bool isValidMove(int fromX, int fromY, int toX, int toY, const Chessboard& board) const {
        if (!isDiagonalMove(fromX, fromY, toX, toY)) {
            return false;
        }

        return isValidVerticalOrHorizontalMove(fromX, fromY, toX, toY, board);
    }
};

class Rook : public ChessPiece {
public:
    Rook(Color _color) : ChessPiece(PieceType::Rook, _color) {}

    bool isValidMove(int fromX, int fromY, int toX, int toY, const Chessboard& board) const {
        if (!isVerticalOrHorizontalMove(fromX, fromY, toX, toY)) {
            return false;
        }

        return isValidVerticalOrHorizontalMove(fromX, fromY, toX, toY, board);
    }
};


int main() {
    //we can implement main function here
    
}
